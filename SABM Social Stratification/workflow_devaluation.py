from SABM.Utils.Implement_Tools import display
from SABM.Utils.Text_Processing import calculation
from SABM.Utils.Text_Processing import format_prompt
from SABM.Class.company import company
from SABM.Class.worker import worker
import matplotlib.pyplot as plt
import SABM.Class.rules as rules
from typing import List

def task(task_parameters, api_key = ''):
    # Definition of Agents
    
    ## Generate agent gender
    gender_list, nf, nm = calculation.generate_gender_list(task_parameters['n_agents'], task_parameters['f_ratio'])
    background_list = calculation.generate_background_list(task_parameters['n_agents'], task_parameters['properties_agents'])
    initial_job_list:list = calculation.generate_initial_job_list(task_parameters['n_agents'], task_parameters['n_jobs'], task_parameters['job_initial_distribution'])
    initial_job_type = list(set(initial_job_list))

    ## Initialize workers and companies
    Na = task_parameters['n_agents']
    Nc = task_parameters['n_jobs']
    workers:List[worker] = []
    companies:List[company] = []

    for i in range(0, Na):
        workers.append(worker(id = i + 1,
                              gender = gender_list[i], background = format_prompt.format_properties(background_list, i), job = initial_job_list[i],
                              model = task_parameters['model'], api_key = api_key, max_tokens = task_parameters['max_tokens']))
    
    for i in range(0, Nc):
        companies.append(company(id = i + 1, n_agents = Na, job_type = initial_job_type[i]))
    
    for w in workers:
        for c in companies:
            if w.job == c.job_type:
                c.member_id.append(w.id)
                w.update_income(c.salary)
                break
    
    for c in companies:
        c.update_member()
        company_gender_list = []
        for wid in c.member_id:
            company_gender_list.append(workers[wid - 1].gender)
        c.NVratio = calculation.calu_NVratio(company_gender_list)
        c.NVratio_history.append(c.NVratio)
        c.member_number_history.append(len(c.member_id))
        c.salary_history.append(c.salary)
    
    ## Setup persona (fixxx)

    ## Summarize the setup
    if task_parameters["info_display"] and True:
        for w in range(min(len(workers), 3)):
            workers[w].info_display()
        for c in companies:
            c.info_display()
        print()
    
    # Definition of Environment
    ## Job data update (if necessary)
    
    # Program Environment Settings
    output_path = task_parameters['record_path'] + '/' + task_parameters['record_name']
    plt.ion()

    # Initialize Prompts
    for w in workers:
        w.init_command(task_parameters)
    if task_parameters["info_display"]:
        display.display(workers[0], display.display_prompt(workers[0].command, task_parameters['order_set']), 'info', 'prompt template')

    # Load Data
        
    #return # Check the prompts

    # Main Loop
    loop_max = task_parameters["loop_max"]
    loop_breakpoint = task_parameters["loop_breakpoint"]
    start_round = task_parameters['start_round']

    for loop_round in range(start_round, loop_max):
        # Break every loop_breakpoint rounds
        if task_parameters["info_display"]: display.display_round(loop_round)
        if display.breakpoint(loop_round, loop_breakpoint):
            break
        tm_flag = False # Terminate flag

        # Phase 1: Work and Background Prompt
        if task_parameters["info_display"]: display.display_phase(loop_round, 'work')
        for w in workers:
            w.update_asset()
            background_prompt = w.background_prompt(task_parameters)
            w.context_prompt = background_prompt
            w.response_history.append({})
        
        # Phase 2: Evaluation
        if task_parameters["info_display"]: display.display_phase(loop_round, 'evaluation')
        
        ## Phase 2-1: Evaluation Self
        for w in workers:
            ### info fixxx
            gender_ratio = 0
            for c in companies:
                if w.id in c.member_id:
                    gender_ratio = c.NVratio
                    break
            
            info = {'loop_round': loop_round, 'all_salaries': calculation.calu_all_salaries(companies), 'all_increases': calculation.calu_all_increases(companies), 'self_gender_ratio': gender_ratio}

            w.evaluation_current(task_parameters, info)

        ## Phase 2-2: Evaluation Others
        for w in workers:
            info = {'loop_round': loop_round, 'all_salaries': calculation.calu_all_salaries(companies), 'other_company_data': calculation.calu_other_data(companies, w.job)}

            w.evaluation_other(task_parameters, info)
        
        # Phase 3: Transfer
        if task_parameters["info_display"]: display.display_phase(loop_round, 'transfer')
        for w in workers:
            ## Transfer decision
            info = {'loop_round': loop_round, 'other_company_names': calculation.calu_other_company_name(companies, w.job)}
            transfer_decision = w.decision_transfer(task_parameters, info)

            ## Target decision
            if transfer_decision:
                target_company = w.decision_transfer_target(task_parameters, info)
            
            ## Rule-based company decision
                offer = False
                for c in companies:
                    if c.id == target_company:
                        ### Agent response error
                        if w.id in c.member_id:
                            break
                        else:
                            ### Target company reaches maximum
                            if len(c.member_id) == c.max_member:
                                break
                            ### Decide Offer
                            else:
                                curr_company_type = ""
                                for cc in companies:
                                    if w.job == cc.job_type:
                                        curr_company_type = cc.company_type
                                        break
                                offer = rules.transfer_offer(w, curr_company_type, c.company_type)
                                break
                
                if offer:
                    for c in companies:
                        if w.id in c.member_id:
                            c.remove_member(w.id)
                    for c in companies:
                        if c.id == target_company:
                            c.member_id.append(w.id)
                            c.update_member()
                            w.job = c.job_type
                            w.transfer_history.append([loop_round, c.id])
        
        # Phase 4: Settlement
        if task_parameters["info_display"]: display.display_phase(loop_round, 'settlement')

        ## Update of Income (fixxx)

        ## Update of Agent Info
        for c in companies:
            for wid in c.member_id:
                workers[wid - 1].update_income(c.salary)
            
            company_gender_list = []
            for wid in c.member_id:
                company_gender_list.append(workers[wid - 1].gender)
            c.NVratio = calculation.calu_NVratio(company_gender_list)
            c.NVratio_history.append(c.NVratio)

            c.member_number_history.append(len(c.member_id))
            print(f"Company {c.job_type} [Type {c.company_type}]: {c.member_number_history[-1]} ({c.member_id}) with N-V ratio {c.NVratio}")

        # Data processing
        ## Save data

        # Terminate Condition
        if tm_flag: break

    plt.close()
    if task_parameters["info_display"]: display.display_results(0)
