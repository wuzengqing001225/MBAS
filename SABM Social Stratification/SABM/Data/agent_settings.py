job_data = {
    # Job title: [Type (Viron, Nymia, Neutral), Description, Annual Salary, Max Member Ratio, Gender Ratio]
    # Ratio is Viron ratio and Nymia ratio respectively, e.g., 90% Astrobiologist are Viron
    "Quantum Network Engineer": ["Viron", "Engineers who design and maintain quantum communication networks for ultra-secure and instantaneous data transmission.", 120000, 0.9, 0.90],
    "Elementary School Teacher": ["Nymia", "Educators who teach young children in elementary schools, covering a variety of subjects.", 50000, 0.9, 0.80],
    "Astrobiologist": ["Viron", "Scientists who study life in the universe, including searching for extraterrestrial life and studying the biology of space habitats.", 95000, 0.6, 0.90],
    "Nurse Practitioner": ["Nymia", "Advanced practice registered nurses who provide primary and specialty healthcare.", 110000, 0.6, 0.85],
    "Petroleum Engineer": ["Viron", "Engineers who develop techniques for extracting oil and gas from deposits below the Earth's surface.", 130000, 0.6, 0.85],
    "Human Resources Manager": ["Nymia", "Professionals who oversee the recruitment, training, and welfare of a company's employees.", 95000, 0.6, 0.75],
    "Aerospace Engineer": ["Viron", "Specialists in the design, testing, and production of aircraft, spacecraft, and missile systems.", 115000, 0.6, 0.88],
    "Social Media Manager": ["Nymia", "Individuals responsible for creating and managing content across social media platforms for brands and companies.", 60000, 0.6, 0.70],
    "Cybersecurity Specialist": ["Viron", "Experts who protect organizations' computer systems and networks from information breaches and cyber-attacks.", 105000, 0.6, 0.80],
    "Interior Designer": ["Nymia", "Designers who plan, research, coordinate, and manage such projects to enhance the interior of a space for aesthetic appeal.", 55000, 0.6, 0.75]
}

# Subject to change to prevent bias / preknowledge (race)
agent_property = {
    "p_education": {
        'Less than High School': 0.12,
        'High School Graduate': 0.30,
        'Associate\'s Degree': 0.29,
        'Bachelor\'s Degree': 0.20,
        'Advanced Degree': 0.09
    },
    "p_race": {
        'White': 0.60,
        'Black or African American': 0.13,
        'Hispanic or Latino': 0.18,
        'Asian': 0.06,
        'Native American or Alaska Native': 0.02,
        'Native Hawaiian or Other Pacific Islander': 0.01
    },
    "p_personalities": {
        "Optimist": 0.5,
        "Pessimistic": 0.5,
    }
}
