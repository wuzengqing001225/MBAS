from SABM.Utils.Implement_Tools.display import display_error
import SABM.Data.agent_settings as agent_data
import random

def calu_grouped_agent_number(n, ratio):
    n = int(n)
    if ratio < 0 or ratio > 1:
        display_error("Gender ratio error", "calculation", "parameter")
        ratio = 0.5
    nf = int(n * ratio)
    nm = n - nf
    return nf, nm

def generate_gender_list(n, ratio):
    nf, nm = calu_grouped_agent_number(n, ratio)

    gender_list = ['Viron'] * nf + ['Nymia'] * nm
    random.shuffle(gender_list)

    return gender_list, nf, nm

def generate_population(n, population_ratio, even_distribution = False):
    population = []
    total = 0.0

    for ratio in population_ratio.values():
        if isinstance(ratio, list): ratio = ratio[-1]
        total += ratio

    if even_distribution == False:
        for property, ratio in population_ratio.items():
            if isinstance(ratio, list): ratio = ratio[-1]
            property_count = int(n * (ratio / total))
            population.extend([property] * property_count)
    else:
        even_ratio = 1 / len(population_ratio.values())
        for property, ratio in population_ratio.items():
            property_count = int(n * even_ratio)
            population.extend([property] * property_count)

    diff = n - len(population)
    if diff != 0:
        last_property = list(population_ratio.keys())[-1]
        population.extend([last_property] * diff)
    
    random.shuffle(population)
    return population

def generate_background_list(n, properties_agents):
    background_list = {}

    for property, distribution in properties_agents.items():
        if distribution == -1:
            background_list[property] = [None] * n
        elif n < len(agent_data.agent_property[property].keys()):
            background_list[property] = list(agent_data.agent_property[property].keys())[:n]
        else:
            if distribution == 0:
                background_list[property] = generate_population(n, agent_data.agent_property[property], True)
            else:
                background_list[property] = generate_population(n, agent_data.agent_property[property])
    
    return background_list

def get_first_m_elements(dictionary, m):
    return {key: dictionary[key] for key in list(dictionary.keys())[:m]}

def generate_initial_job_list(n, n_jobs, job_initial_distribution):
    if n_jobs > n:
        display_error("n_jobs error", "calculation", "parameter")
        n_jobs = n
    
    if job_initial_distribution == 0:
        agent_data.job_data = get_first_m_elements(agent_data.job_data, n_jobs)
        return generate_population(n, agent_data.job_data, True)
    else:
        display_error("Not Implemented", "calculation")
        agent_data.job_data = get_first_m_elements(agent_data.job_data, n_jobs)
        return generate_population(n, agent_data.job_data)

def calu_income_difference(income_history):
    if len(income_history) == 1: return 0
    else: return income_history[-1] - income_history[-2]

def calu_salary_bin(data_list, company_salary):
    sorted_data = sorted(data_list)
    total_count = len(sorted_data)

    if total_count <= 5:
        return "Bottom 50%" if company_salary <= sorted_data[total_count // 2 - 1] else "Top 50%"
    
    bin20_index = total_count // 5
    bin40_index = bin20_index * 2
    bin60_index = bin20_index * 3
    bin_last40_index = total_count - bin20_index
    bin_last20_index = total_count - (total_count // 5)
    
    if company_salary <= sorted_data[bin20_index - 1]:
        return "Bottom 20%"
    elif company_salary <= sorted_data[bin40_index - 1]:
        return "Bottom 20%-40%"
    elif company_salary <= sorted_data[bin60_index - 1]:
        return "Top 40%-60%"
    elif company_salary <= sorted_data[bin_last40_index]:
        return "Top 20%-40%"
    else:
        return "Top 20%"

def calu_increase_bin(data_list, value):
    median = sorted(data_list)[len(data_list) // 2]
    if value >= median:
        return "higher"
    else:
        return "lower"
    
def calu_NVratio(gender_list):
    sum_N = 0.0
    sum_V = 0.0

    for g in gender_list:
        if g == "Nymia": sum_N += 1.0
        elif g == "Viron": sum_V += 1.0
    
    if sum_V == 0: return "infinity"
    else: return round(sum_N / sum_V, 2)

def calu_all_salaries(company_list):
    all_salaries = []
    for c in company_list:
        all_salaries.append(c.salary)
    return all_salaries

def calu_all_increases(company_list):
    all_increases = []
    for c in company_list:
        if len(c.salary_history) == 1: all_increases.append(0)
        else:
            all_increases.append(c.salary_history[-1] - c.salary_history[-2])
    return all_increases

def calu_other_data(company_list, skip_company):
    data = ""
    for c in company_list:
        if c.job_type == skip_company: pass
        else:
            data += f"{c.job_type}: [{c.salary}, {c.NVratio}]\n"
    return data

def calu_other_company_name(company_list, skip_company):
    company_name = ""
    for c in company_list:
        if c.job_type == skip_company: pass
        else:
            company_name += f"[{c.id}: {c.job_type}] "
    return company_name