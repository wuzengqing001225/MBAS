prompt_task = {
    "task_0": {
        "task": "You act as a worker.",
        "objective assumption": "You have many job skills and a certain desire to seek higher paying jobs.",
        "information assumption": "You know all the possible companies you can go to and the distribution of their companies and people.",
        "gender background": "There are two types of workers, Viron and Nymia.",
    }
}

prompt_role = {
    "role_default": {
        "reference": "You are a {worker_type}.",
        "role": "You need to evaluate different companies based on the information gathered, identify career advancement opportunities, and decide whether to transfer for a more satisfying job (in terms of reputation, salary, etc.).",
        "restriction": "Of course, switching industries is quite challenging, as it depends on your current employer and other factors."
    }
}

prompt_history = {
    "history_self_company": {
        "salary": "Your company's salary stands at {salary}, ranking in the {percentage} among all companies.",
        "comparison": "It has increased by {increase_amount} compared to last month and is {comparison} than other companies.",
        "gender": "The ratio of Nymia to Viron employees in your company is {gender_ratio}."
    },
    "history_other_companies": {
        "salary": "Your company's salary stands at {salary}, ranking in the {percentage} among all companies.",
        "info": "Information about other companies is in the format (Company Name: [Salary, Ratio of Viron to Nymia employees]):\n{companies_data}"
    },
    "history_evaluation": {
        "self": "Previously you evaluated your company's situation: '{self_eval}'.",
        "others": "\nYou also evaluated other companies as:\n'{other_eval}'.",
    },
    "history_evaluation_target": "You evaluated other companies as '{other_eval}'.",
}

prompt_action = {
    "action_evaluation_self": "How would you evaluate your current company's reputation, salary, and other standards based on these information?",
    "action_evaluation_other": "Based on this information, what do you think about other companies? What will be the career trends afterward?",
    "action_decision_transfer": "Based on your evaluation, would you like to transfer to other companies?",
    "action_decision_target": "Based on your evaluation, which of the following companies would you like to move from (format [number: company])?\n{target_list}",
}

prompt_output = {
    "output_limit": "Please describe your idea concisely in {limit_token} tokens.",
    "output_evaluation_other": "Please provide a brief review of each of the other companies, with one line indicating one company.",
    "output_bool": "Only answer 'Yes' or 'No' without any reasoning.",
    "output_number_target": "Answer only one number that indicates the company you choose.",
    "output_ban": "Please do not use any units or symbols, and avoid providing any additional context or explanation in your response.",
}

prompt_rule = {

}

task_prompt = {
    "task": prompt_task,
    "role": prompt_role,
    "history": prompt_history,
    "action": prompt_action,
    "output": prompt_output,
    "rule": prompt_rule,
}
