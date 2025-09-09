"""
Django Management Command to Populate Database with Dummy Data
Place this file in: management/commands/populate_dummy_data.py
Run with: python manage.py populate_dummy_data
"""

import random
import string
import json
from datetime import datetime, timedelta, date
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from faker import Faker

# Import all your models
from home.models import (
    AdminNotification, APIModel, User, PasswordHistory,
    Webpage, Project, Course, Skill, Student, Progress,
    Contact, DDT_contact, Article, Smishingdetection_join_us,
    Projects_join_us, Profile, CyberChallenge, UserChallenge,
    BlogPost, Announcement, SecurityEvent, ExampleModel,
    ContactSubmission, Job, JobAlert, GraduateProgram,
    CareerFAQ, JobApplication, LeaderBoardTable, Experience,
    UserBlogPage, Report, Passkey, AppAttackReport,
    PenTestingRequest, SecureCodeReviewRequest, AdminSession
)

fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = 'Populates database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting dummy data population...')
        
        with transaction.atomic():
            # Create users first
            users = self.create_users()
            
            # Create core entities
            projects = self.create_projects()
            courses = self.create_courses()
            skills = self.create_skills()
            
            # Create students and relationships
            students = self.create_students(users, projects)
            self.create_progress(students, skills)
            
            # Create content
            self.create_articles(users)
            self.create_cyber_challenges()
            self.create_user_challenges(users)
            self.create_blog_posts()
            self.create_jobs()
            self.create_job_applications()
            self.create_graduate_programs()
            self.create_career_faqs()
            
            # Create various submissions
            self.create_contacts()
            self.create_experiences()
            self.create_announcements()
            self.create_security_events(users)
            self.create_admin_notifications(users)
            self.create_webpages()
            self.create_api_models()
            self.create_job_alerts()
            self.create_leaderboard(users)
            self.create_user_blog_pages()
            self.create_reports()
            self.create_pen_testing_requests()
            self.create_secure_code_reviews()
            self.create_admin_sessions(users)
            
        self.stdout.write(self.style.SUCCESS('Successfully populated dummy data!'))

    def create_users(self):
        """Create various types of users"""
        users = []
        
        # Create superuser
        if not User.objects.filter(email='admin@deakin.edu.au').exists():
            superuser = User.objects.create_superuser(
                email='admin@deakin.edu.au',
                password='admin123',
                first_name='Admin',
                last_name='User',
                is_verified=True
            )
            users.append(superuser)
            self.stdout.write(f'Created superuser: admin@deakin.edu.au')
        
        # Create staff users
        for i in range(3):
            email = f'staff{i+1}@deakin.edu.au'
            if not User.objects.filter(email=email).exists():
                staff = User.objects.create_user(
                    email=email,
                    password='staff123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    is_staff=True,
                    is_verified=True
                )
                users.append(staff)
        
        # Create regular users
        for i in range(20):
            email = f'student{i+1}@deakin.edu.au'
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    password='student123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    is_verified=random.choice([True, False]),
                    upskilling_progress={
                        'python': random.randint(0, 100),
                        'cybersecurity': random.randint(0, 100),
                        'web_development': random.randint(0, 100)
                    }
                )
                
                # Create profile for each user
                Profile.objects.create(
                    user=user,
                    bio=fake.text(max_nb_chars=200),
                    linkedin=f'https://linkedin.com/in/{user.first_name.lower()}{user.last_name.lower()}',
                    github=f'https://github.com/{user.first_name.lower()}{i}',
                    location=fake.city()
                )
                
                # Generate passkeys for verified users
                if user.is_verified:
                    for _ in range(5):
                        Passkey.objects.create(
                            user=user,
                            key=''.join(random.choices(string.ascii_letters + string.digits, k=12))
                        )
                
                users.append(user)
        
        self.stdout.write(f'Created {len(users)} users')
        return users

    def create_projects(self):
        """Create projects"""
        projects = []
        project_data = [
            ('AppAttack', 'Mobile application security testing framework'),
            ('Malware', 'Malware analysis and detection system'),
            ('PT-GUI', 'Penetration testing GUI tool'),
            ('Smishing_Detection', 'SMS phishing detection system'),
            ('Deakin_CyberSafe_VR', 'Virtual reality cybersecurity training'),
            ('Deakin_Threat_Mirror', 'Threat intelligence platform'),
            ('Company_Website_Development', 'Corporate website development project')
        ]
        
        for title, desc in project_data:
            project, created = Project.objects.get_or_create(
                title=title,
                defaults={'description': desc, 'archived': random.choice([True, False, False])}
            )
            projects.append(project)
        
        self.stdout.write(f'Created {len(projects)} projects')
        return projects

    def create_courses(self):
        """Create courses"""
        courses = []
        course_data = [
            ('Bachelor of Computer Science', 'BCS', False),
            ('Bachelor of Cyber Security', 'BCYB', False),
            ('Bachelor of Information Technology', 'BIT', False),
            ('Master of Cyber Security', 'MCS', True),
            ('Master of Information Technology', 'MIT', True),
            ('Master of Data Science', 'MDS', True)
        ]
        
        for title, code, is_pg in course_data:
            course, created = Course.objects.get_or_create(
                code=code,
                defaults={'title': title, 'is_postgraduate': is_pg}
            )
            courses.append(course)
        
        self.stdout.write(f'Created {len(courses)} courses')
        return courses

    def create_skills(self):
        """Create skills"""
        skills = []
        skill_data = [
            ('Python Programming', 'Advanced Python programming techniques'),
            ('Web Security', 'Web application security testing'),
            ('Network Security', 'Network security and penetration testing'),
            ('Cryptography', 'Cryptographic algorithms and protocols'),
            ('Machine Learning', 'ML for cybersecurity applications'),
            ('Cloud Security', 'AWS and Azure security'),
            ('Forensics', 'Digital forensics and incident response'),
            ('Secure Coding', 'Secure software development practices')
        ]
        
        for name, desc in skill_data:
            skill, created = Skill.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'slug': name.lower().replace(' ', '-')}
            )
            skills.append(skill)
        
        self.stdout.write(f'Created {len(skills)} skills')
        return skills

    def create_students(self, users, projects):
        """Create student records"""
        students = []
        regular_users = [u for u in users if not u.is_staff and not u.is_superuser]
        
        for i, user in enumerate(regular_users[:15]):  # Create 15 students
            student_id = 220000000 + i
            
            # Randomly select 3 different projects for preferences
            selected_projects = random.sample(projects, 3)
            
            student, created = Student.objects.get_or_create(
                id=student_id,
                defaults={
                    'user': user,
                    'year': random.randint(2022, 2025),
                    'trimester': random.choice(['T1', 'T2', 'T3']),
                    'unit': random.choice(['SIT782', 'SIT764', 'SIT378', 'SIT374']),
                    'course': random.choice(['BCS', 'BCYB', 'BIT', 'MCS', 'MIT', 'MDS']),
                    'p1': selected_projects[0],
                    'p2': selected_projects[1],
                    'p3': selected_projects[2],
                    'allocated': random.choice(selected_projects)
                }
            )
            students.append(student)
        
        self.stdout.write(f'Created {len(students)} students')
        return students

    def create_progress(self, students, skills):
        """Create progress records for students"""
        progress_count = 0
        for student in students:
            # Each student progresses in 3-5 random skills
            selected_skills = random.sample(skills, random.randint(3, 5))
            for skill in selected_skills:
                progress_val = random.randint(0, 100)
                Progress.objects.create(
                    student=student,
                    skill=skill,
                    progress=progress_val,
                    completed=progress_val == 100
                )
                progress_count += 1
        
        self.stdout.write(f'Created {progress_count} progress records')

    def create_articles(self, users):
        """Create articles"""
        articles = []
        authors = [u for u in users if u.is_staff or u.is_superuser]
        
        for i in range(15):
            article = Article.objects.create(
                title=fake.sentence(nb_words=6),
                content=f'<p>{fake.text(max_nb_chars=2000)}</p>',
                author=random.choice(authors),
                featured=random.choice([True, False, False])
            )
            # Add random likes
            likers = random.sample(users, random.randint(0, 10))
            article.likes.set(likers)
            articles.append(article)
        
        self.stdout.write(f'Created {len(articles)} articles')

    def create_cyber_challenges(self):
        """Create cyber challenges"""
        challenges = []
        
        # MCQ challenges
        mcq_data = [
            {
                'title': 'SQL Injection Basics',
                'description': 'Test your knowledge of SQL injection attacks',
                'question': 'Which of the following is a common SQL injection prevention technique?',
                'choices': ['Input validation', 'Using admin/admin', 'Disabling the database', 'Removing all forms'],
                'correct_answer': 'Input validation',
                'difficulty': 'easy',
                'category': 'web_security',
                'challenge_type': 'mcq',
                'points': 10
            },
            {
                'title': 'Cryptography Fundamentals',
                'description': 'Understanding basic cryptographic concepts',
                'question': 'What type of encryption uses the same key for encryption and decryption?',
                'choices': ['Asymmetric', 'Symmetric', 'Hashing', 'Digital Signature'],
                'correct_answer': 'Symmetric',
                'difficulty': 'easy',
                'category': 'crypto',
                'challenge_type': 'mcq',
                'points': 10
            }
        ]
        
        # Fix code challenges
        fix_code_data = [
            {
                'title': 'Fix the Python Bug',
                'description': 'Debug this Python function',
                'starter_code': 'def add_numbers(a, b):\n    return a + b',
                'sample_input': '5, 3',
                'expected_output': '8',
                'difficulty': 'easy',
                'category': 'python',
                'challenge_type': 'fix_code',
                'points': 15
            }
        ]
        
        for mcq in mcq_data:
            challenge = CyberChallenge.objects.create(**mcq)
            challenges.append(challenge)
        
        for code in fix_code_data:
            challenge = CyberChallenge.objects.create(**code)
            challenges.append(challenge)
        
        self.stdout.write(f'Created {len(challenges)} cyber challenges')

    def create_user_challenges(self, users):
        """Create user challenge attempts"""
        challenges = CyberChallenge.objects.all()
        user_challenges = []
        
        for user in random.sample(users, min(10, len(users))):
            for challenge in random.sample(list(challenges), min(2, len(challenges))):
                uc = UserChallenge.objects.create(
                    user=user,
                    challenge=challenge,
                    completed=random.choice([True, False]),
                    score=random.randint(0, challenge.points)
                )
                user_challenges.append(uc)
        
        self.stdout.write(f'Created {len(user_challenges)} user challenge attempts')

    def create_blog_posts(self):
        """Create blog posts"""
        blog_posts = []
        pages = ['home', 'about', 'services', 'blog', 'contact']
        
        for i in range(20):
            post = BlogPost.objects.create(
                title=fake.sentence(nb_words=6),
                body=fake.text(max_nb_chars=1000),
                page_name=random.choice(pages)
            )
            blog_posts.append(post)
        
        self.stdout.write(f'Created {len(blog_posts)} blog posts')

    def create_jobs(self):
        """Create job listings"""
        jobs = []
        job_titles = [
            'Senior Security Engineer',
            'Junior Penetration Tester',
            'Cloud Security Architect',
            'SOC Analyst',
            'Security Software Developer',
            'Incident Response Specialist'
        ]
        
        for title in job_titles:
            job = Job.objects.create(
                title=title,
                description=f'<p>{fake.text(max_nb_chars=500)}</p>',
                location=random.choice(['Remote', 'OnSite', 'Hybrid']),
                job_type=random.choice(['FT', 'PT', 'CT', 'internship']),
                closing_date=timezone.now().date() + timedelta(days=random.randint(30, 90)),
                responsibilities=f'<ul><li>{fake.sentence()}</li><li>{fake.sentence()}</li></ul>',
                qualifications=f'<ul><li>{fake.sentence()}</li><li>{fake.sentence()}</li></ul>',
                benefits=f'<ul><li>{fake.sentence()}</li><li>{fake.sentence()}</li></ul>',
                salary_range='$80,000 - $120,000',
                experience_level=random.choice(['entry', 'mid', 'senior', 'lead']),
                department='Cybersecurity',
                skills_required='Python, Network Security, Linux'
            )
            jobs.append(job)
        
        self.stdout.write(f'Created {len(jobs)} jobs')
        return jobs

    def create_job_applications(self):
        """Create job applications"""
        jobs = Job.objects.all()
        applications = []
        
        for job in jobs:
            for i in range(random.randint(1, 5)):
                app = JobApplication.objects.create(
                    job=job,
                    name=fake.name(),
                    email=fake.email(),
                    resume='resumes/dummy_resume.pdf',
                    cover_letter='cover_letter/dummy_cover.pdf'
                )
                applications.append(app)
        
        self.stdout.write(f'Created {len(applications)} job applications')

    def create_graduate_programs(self):
        """Create graduate programs"""
        programs = []
        program_data = [
            ('Cybersecurity Graduate Program', 'cybersecurity', 12),
            ('Software Engineering Graduate Program', 'software_engineering', 18),
            ('Data Science Graduate Program', 'data_science', 12)
        ]
        
        for title, prog_type, duration in program_data:
            program = GraduateProgram.objects.create(
                title=title,
                description=f'<p>{fake.text(max_nb_chars=300)}</p>',
                duration_months=duration,
                program_type=prog_type,
                start_date=timezone.now().date() + timedelta(days=90),
                application_deadline=timezone.now().date() + timedelta(days=60),
                overview=f'<p>{fake.text(max_nb_chars=500)}</p>',
                curriculum=f'<p>{fake.text(max_nb_chars=500)}</p>',
                benefits=f'<p>{fake.text(max_nb_chars=300)}</p>',
                requirements=f'<p>{fake.text(max_nb_chars=300)}</p>',
                application_process=f'<p>{fake.text(max_nb_chars=300)}</p>'
            )
            programs.append(program)
        
        self.stdout.write(f'Created {len(programs)} graduate programs')

    def create_career_faqs(self):
        """Create career FAQs"""
        faqs = []
        faq_data = [
            ('How do I apply for a position?', 'application', True),
            ('What benefits do you offer?', 'benefits', True),
            ('What are the growth opportunities?', 'growth', False),
            ('Do you offer remote work?', 'general', True),
            ('What is the interview process?', 'application', False)
        ]
        
        for question, category, popular in faq_data:
            faq = CareerFAQ.objects.create(
                question=question,
                answer=f'<p>{fake.text(max_nb_chars=300)}</p>',
                category=category,
                is_popular=popular,
                order=random.randint(1, 10)
            )
            faqs.append(faq)
        
        self.stdout.write(f'Created {len(faqs)} career FAQs')

    def create_contacts(self):
        """Create contact submissions"""
        contacts = []
        
        for i in range(10):
            contact = Contact.objects.create(
                name=fake.name(),
                email=fake.email(),
                message=fake.text(max_nb_chars=500)
            )
            contacts.append(contact)
        
        for i in range(5):
            ddt_contact = DDT_contact.objects.create(
                fullname=fake.name(),
                email=fake.email(),
                mobile=fake.phone_number(),
                message=fake.text(max_nb_chars=300)
            )
        
        for i in range(8):
            contact_sub = ContactSubmission.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                message=fake.text(max_nb_chars=400)
            )
        
        self.stdout.write('Created contact submissions')

    def create_experiences(self):
        """Create user experiences/feedback"""
        experiences = []
        
        for i in range(15):
            exp = Experience.objects.create(
                name=fake.name(),
                feedback=fake.text(max_nb_chars=300),
                rating=random.randint(1, 5)
            )
            experiences.append(exp)
        
        self.stdout.write(f'Created {len(experiences)} experiences')

    def create_announcements(self):
        """Create announcements"""
        announcements = []
        
        for i in range(5):
            announcement = Announcement.objects.create(
                message=fake.sentence(nb_words=15),
                isActive=random.choice([True, False])
            )
            announcements.append(announcement)
        
        self.stdout.write(f'Created {len(announcements)} announcements')

    def create_security_events(self, users):
        """Create security events"""
        events = []
        event_types = ['login_success', 'login_failure', 'password_change', 'suspicious_activity']
        
        for i in range(30):
            event = SecurityEvent.objects.create(
                user=random.choice(users) if random.random() > 0.1 else None,
                event_type=random.choice(event_types),
                ip_address=fake.ipv4(),
                details=fake.text(max_nb_chars=100)
            )
            events.append(event)
        
        self.stdout.write(f'Created {len(events)} security events')

    def create_admin_notifications(self, users):
        """Create admin notifications"""
        notifications = []
        
        for i in range(10):
            notification = AdminNotification.objects.create(
                title=fake.sentence(nb_words=5),
                message=fake.text(max_nb_chars=200),
                notification_type=random.choice(['feedback', 'update', 'alert', 'info']),
                is_read=random.choice([True, False]),
                related_user=random.choice(users) if random.random() > 0.5 else None
            )
            notifications.append(notification)
        
        self.stdout.write(f'Created {len(notifications)} admin notifications')

    def create_webpages(self):
        """Create webpage entries"""
        webpages = []
        pages = [
            ('/home', 'Home'),
            ('/about', 'About Us'),
            ('/services', 'Our Services'),
            ('/contact', 'Contact'),
            ('/careers', 'Careers')
        ]
        
        for url, title in pages:
            webpage, created = Webpage.objects.get_or_create(
                url=url,
                defaults={'title': title}
            )
            webpages.append(webpage)
        
        self.stdout.write(f'Created {len(webpages)} webpages')

    def create_api_models(self):
        """Create API model entries"""
        api_models = []
        
        for i in range(5):
            api_model = APIModel.objects.create(
                name=f'API Endpoint {i+1}',
                field_name=f'field_{i+1}',
                description=fake.text(max_nb_chars=200)
            )
            api_models.append(api_model)
        
        self.stdout.write(f'Created {len(api_models)} API models')

    def create_job_alerts(self):
        """Create job alert subscriptions"""
        alerts = []
        
        for i in range(20):
            alert, created = JobAlert.objects.get_or_create(
                email=fake.email(),
                defaults={'is_active': random.choice([True, False])}
            )
            if created:
                alerts.append(alert)
        
        self.stdout.write(f'Created {len(alerts)} job alerts')

    def create_leaderboard(self, users):
        """Create leaderboard entries"""
        entries = []
        categories = ['Python', 'Web Security', 'Cryptography', 'Network Security', 'Overall']
        
        for user in random.sample(users, min(15, len(users))):
            for category in random.sample(categories, random.randint(1, 3)):
                entry = LeaderBoardTable.objects.create(
                    user=user,
                    category=category,
                    total_points=random.randint(0, 1000)
                )
                entries.append(entry)
        
        self.stdout.write(f'Created {len(entries)} leaderboard entries')

    def create_user_blog_pages(self):
        """Create user blog pages"""
        blog_pages = []
        
        for i in range(10):
            blog_page = UserBlogPage.objects.create(
                name=fake.name(),
                title=fake.sentence(nb_words=6),
                description=fake.text(max_nb_chars=500),
                file='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==',
                isShow=random.choice([True, False])
            )
            blog_pages.append(blog_page)
        
        self.stdout.write(f'Created {len(blog_pages)} user blog pages')

    def create_reports(self):
        """Create report entries"""
        reports = []
        
        for i in range(5):
            report = Report.objects.create(
                blog_id=random.randint(1, 10),
                blog_name=fake.sentence(nb_words=4),
                reason=fake.text(max_nb_chars=200)
            )
            reports.append(report)
        
        self.stdout.write(f'Created {len(reports)} reports')

    def create_pen_testing_requests(self):
        """Create penetration testing requests"""
        requests = []
        
        for i in range(8):
            request = PenTestingRequest.objects.create(
                name=fake.name(),
                email=fake.email(),
                github_repo_link=f'https://github.com/{fake.user_name()}/repo',
                project_description=fake.text(max_nb_chars=300),
                terms_accepted=True
            )
            requests.append(request)
        
        self.stdout.write(f'Created {len(requests)} pen testing requests')

    def create_secure_code_reviews(self):
        """Create secure code review requests"""
        reviews = []
        
        for i in range(6):
            review = SecureCodeReviewRequest.objects.create(
                name=fake.name(),
                email=fake.email(),
                github_repo_link=f'https://github.com/{fake.user_name()}/project',
                project_description=fake.text(max_nb_chars=300),
                terms_accepted=True
            )
            reviews.append(review)
        
        self.stdout.write(f'Created {len(reviews)} secure code review requests')

    def create_admin_sessions(self, users):
        """Create admin session records"""
        sessions = []
        admin_users = [u for u in users if u.is_staff or u.is_superuser]
        
        for admin in admin_users[:5]:
            session = AdminSession.objects.create(
                user=admin,
                session_key=''.join(random.choices(string.ascii_letters + string.digits, k=40)),
                ip_address=fake.ipv4(),
                user_agent=fake.user_agent(),
                is_active=random.choice([True, False])
            )
            if not session.is_active:
                session.logout_time = timezone.now()
                session.logout_reason = random.choice(['manual', 'timeout', 'forced'])
                session.save()
            sessions.append(session)
        
        self.stdout.write(f'Created {len(sessions)} admin sessions')