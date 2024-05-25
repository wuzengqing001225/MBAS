prompt_task = {
    "task_default": "Now you are participating in a number-guessing game.",
}

prompt_role = {
    "role_adjudicator": "You are the one responsible for thinking up the numbers.",
    "role_guesser": "You are the one in charge of guessing.",

    "role_adjudicator_continue": "You are participating in a number-guessing game and you are the one responsible for thinking up the numbers.",
    "role_guesser_continue": "You are participating in a number-guessing game and you are the one to guess the number.",
}

prompt_history = {
    "history_adjudicator_target_number": "You decided {target_number} as the answer.",
    "history_adjudicator_guesser_guess": "Your opponent had made a guess of {guess}.",

    "history_guesser_previous_one_guess": "Your previous guess was {previous_guess}",
    "history_guesser_guess_history": "The history of your guess is {guess_history}.",
}

prompt_action = {
    "action_adjudicator": "Please think of an integer, ranging from {range_begin} to {range_end}.",
    "action_guesser": {
        "range": "The number will be an integer ranging from {range_begin} to {range_end}.",
        "info_to_agent": "After you made a guess, you will be informed if your guess is right, higher than the answer, or lower than the answer.",
        "action": "Now please make your first guess.",
    },

    "action_adjudicator_judge": {
        "standard": "Can you tell your opponent if the guess is right, higher than the answer, or lower than the answer?"
    },
    "action_guesser_continue": {
        "range": "The number will be an integer ranging from {range_begin} to {range_end}.",
    },
}

prompt_output = {
    "output_number": "Only reply the number (e.g., 12).",
    "output_guess": "Only reply the number (e.g., 12).",
    "output_judge": "If the guess is correct, please say “Congratulations!”.",
}

task_prompt = {
    "task": prompt_task,
    "role": prompt_role,
    "history": prompt_history,
    "action": prompt_action,
    "output": prompt_output,
}
