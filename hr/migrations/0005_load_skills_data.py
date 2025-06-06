# Generated by Django 5.1.1 on 2025-06-03 22:27

from django.db import migrations


class Migration(migrations.Migration):

    def load_skills(apps, schema_editor):
        Skill = apps.get_model('hr', 'Skill')
        skills_data = [
    # Technical Skills
    {"name": "Python", "category": "technical"},
    {"name": "JavaScript", "category": "technical"},
    {"name": "Java", "category": "technical"},
    {"name": "C#", "category": "technical"},
    {"name": "PHP", "category": "technical"},
    {"name": "Ruby on Rails", "category": "technical"},
    {"name": "SQL", "category": "technical"},
    {"name": "HTML/CSS", "category": "technical"},
    {"name": "React.js", "category": "technical"},
    {"name": "Angular", "category": "technical"},
    {"name": "Node.js", "category": "technical"},
    {"name": "Docker", "category": "technical"},
    {"name": "Kubernetes", "category": "technical"},
    {"name": "AWS", "category": "technical"},
    {"name": "Azure", "category": "technical"},
    {"name": "Google Cloud Platform", "category": "technical"},
    {"name": "Linux Administration", "category": "technical"},
    {"name": "DevOps", "category": "technical"},
    {"name": "Machine Learning", "category": "technical"},
    {"name": "Data Science", "category": "technical"},
    {"name": "Artificial Intelligence", "category": "technical"},
    {"name": "Cybersecurity", "category": "technical"},
    {"name": "Blockchain", "category": "technical"},
    {"name": "Cloud Computing", "category": "technical"},
    {"name": "Database Management", "category": "technical"},

    # Project Management & Leadership
    {"name": "Project Planning", "category": "project_management"},
    {"name": "Risk Management", "category": "project_management"},
    {"name": "Agile Methodology", "category": "project_management"},
    {"name": "Scrum", "category": "project_management"},
    {"name": "Kanban", "category": "project_management"},
    {"name": "Stakeholder Management", "category": "project_management"},
    {"name": "Team Leadership", "category": "project_management"},
    {"name": "Resource Allocation", "category": "project_management"},
    {"name": "Budgeting", "category": "project_management"},
    {"name": "Time Management", "category": "project_management"},
    {"name": "Conflict Resolution", "category": "project_management"},
    {"name": "Communication", "category": "project_management"},
    {"name": "Negotiation", "category": "project_management"},
    {"name": "Problem-Solving", "category": "project_management"},
    {"name": "Critical Thinking", "category": "project_management"},

    # Marketing & Sales
    {"name": "Digital Marketing", "category": "marketing"},
    {"name": "Content Creation", "category": "marketing"},
    {"name": "SEO", "category": "marketing"},
    {"name": "SEM", "category": "marketing"},
    {"name": "Social Media Marketing", "category": "marketing"},
    {"name": "Email Marketing", "category": "marketing"},
    {"name": "Copywriting", "category": "marketing"},
    {"name": "Sales Strategy", "category": "marketing"},
    {"name": "CRM", "category": "marketing"},
    {"name": "Lead Generation", "category": "marketing"},
    {"name": "Market Research", "category": "marketing"},
    {"name": "Brand Management", "category": "marketing"},
    {"name": "PPC", "category": "marketing"},
    {"name": "Affiliate Marketing", "category": "marketing"},
    {"name": "Data Analytics in Marketing", "category": "marketing"},

    # Finance & Accounting
    {"name": "Financial Analysis", "category": "finance"},
    {"name": "Accounting", "category": "finance"},
    {"name": "Budgeting and Forecasting", "category": "finance"},
    {"name": "Payroll Management", "category": "finance"},
    {"name": "Taxation", "category": "finance"},
    {"name": "Auditing", "category": "finance"},
    {"name": "Financial Reporting", "category": "finance"},
    {"name": "Cost Management", "category": "finance"},
    {"name": "Risk Management", "category": "finance"},
    {"name": "Investment Strategies", "category": "finance"},
    {"name": "QuickBooks", "category": "finance"},
    {"name": "Excel (Advanced)", "category": "finance"},
    {"name": "ERP Systems", "category": "finance"},

    # Human Resources
    {"name": "Recruitment", "category": "hr"},
    {"name": "Onboarding", "category": "hr"},
    {"name": "Employee Relations", "category": "hr"},
    {"name": "Payroll Processing", "category": "hr"},
    {"name": "Benefits Administration", "category": "hr"},
    {"name": "Talent Acquisition", "category": "hr"},
    {"name": "Performance Appraisal", "category": "hr"},
    {"name": "Compliance", "category": "hr"},
    {"name": "Training and Development", "category": "hr"},
    {"name": "Succession Planning", "category": "hr"},
    {"name": "Conflict Resolution", "category": "hr"},
    {"name": "Diversity and Inclusion", "category": "hr"},
    {"name": "HR Information Systems", "category": "hr"},

    # Design & Creative
    {"name": "Adobe Photoshop", "category": "design"},
    {"name": "Adobe Illustrator", "category": "design"},
    {"name": "Adobe XD", "category": "design"},
    {"name": "Sketch", "category": "design"},
    {"name": "Figma", "category": "design"},
    {"name": "Video Editing", "category": "design"},
    {"name": "UX/UI Design", "category": "design"},
    {"name": "Graphic Design", "category": "design"},
    {"name": "Motion Graphics", "category": "design"},
    {"name": "3D Modeling", "category": "design"},
    {"name": "Branding", "category": "design"},
    {"name": "Typography", "category": "design"},
    {"name": "Print Design", "category": "design"},
    {"name": "Illustration", "category": "design"},
    {"name": "Web Design", "category": "design"},

    # Customer Service & Support
    {"name": "Customer Relationship Management", "category": "customer_service"},
    {"name": "Call Center Management", "category": "customer_service"},
    {"name": "Conflict Resolution", "category": "customer_service"},
    {"name": "Troubleshooting", "category": "customer_service"},
    {"name": "Client Communication", "category": "customer_service"},
    {"name": "Time Management", "category": "customer_service"},
    {"name": "Problem Solving", "category": "customer_service"},
    {"name": "Multi-tasking", "category": "customer_service"},
    {"name": "Technical Support", "category": "customer_service"},
    {"name": "Ticket Management Systems", "category": "customer_service"},
    {"name": "Help Desk Tools", "category": "customer_service"},

    # Operations & Supply Chain
    {"name": "Supply Chain Management", "category": "operations"},
    {"name": "Inventory Management", "category": "operations"},
    {"name": "Vendor Management", "category": "operations"},
    {"name": "Procurement", "category": "operations"},
    {"name": "Logistics", "category": "operations"},
    {"name": "Quality Control", "category": "operations"},
    {"name": "Lean Manufacturing", "category": "operations"},
    {"name": "Six Sigma", "category": "operations"},
    {"name": "Production Planning", "category": "operations"},
    {"name": "Warehouse Management", "category": "operations"},
    {"name": "Shipping and Receiving", "category": "operations"},

    # Legal & Compliance
    {"name": "Contract Management", "category": "legal"},
    {"name": "Intellectual Property", "category": "legal"},
    {"name": "Corporate Governance", "category": "legal"},
    {"name": "Risk Management", "category": "legal"},
    {"name": "Legal Research", "category": "legal"},
    {"name": "Compliance Management", "category": "legal"},
    {"name": "Labor Law", "category": "legal"},
    {"name": "Regulatory Affairs", "category": "legal"},
    {"name": "Data Privacy", "category": "legal"},
    {"name": "Mergers and Acquisitions", "category": "legal"},
    {"name": "Dispute Resolution", "category": "legal"},
    {"name": "Contract Negotiation", "category": "legal"},

    # Soft Skills
    {"name": "Communication", "category": "soft_skills"},
    {"name": "Teamwork", "category": "soft_skills"},
    {"name": "Problem Solving", "category": "soft_skills"},
    {"name": "Adaptability", "category": "soft_skills"},
    {"name": "Emotional Intelligence", "category": "soft_skills"},
    {"name": "Creativity", "category": "soft_skills"},
    {"name": "Decision Making", "category": "soft_skills"},
    {"name": "Time Management", "category": "soft_skills"},
    {"name": "Conflict Resolution", "category": "soft_skills"},
    {"name": "Leadership", "category": "soft_skills"},
    {"name": "Critical Thinking", "category": "soft_skills"},
    {"name": "Active Listening", "category": "soft_skills"},
    {"name": "Interpersonal Skills", "category": "soft_skills"},
    {"name": "Stress Management", "category": "soft_skills"},
    {"name": "Negotiation", "category": "soft_skills"},

    # Languages
    {"name": "English", "category": "languages"},
    {"name": "Spanish", "category": "languages"},
    {"name": "French", "category": "languages"},
    {"name": "German", "category": "languages"},
    {"name": "Mandarin", "category": "languages"},
    {"name": "Japanese", "category": "languages"},
    {"name": "Russian", "category": "languages"},
    {"name": "Arabic", "category": "languages"},
    {"name": "Hindi", "category": "languages"},
    {"name": "Portuguese", "category": "languages"},
]

        Skill.objects.bulk_create([Skill(name=skill['name'], category=skill['category']) for skill in skills_data])
  
    dependencies = [
        ('hr', '0004_load_public_holidays'),
    ]

    operations = [
        migrations.RunPython(load_skills)
    ]
