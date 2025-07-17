from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random
import uuid
from home.models import (
    AdminNotification, APIModel, User, Webpage, Project, Course, Skill, 
    Student, Contact, DDT_contact, Progress, Article, Smishingdetection_join_us,
    Projects_join_us, Profile, CyberChallenge, UserChallenge, BlogPost,
    Announcement, SecurityEvent, ExampleModel, ContactSubmission, Job,
    JobApplication, LeaderBoardTable, Experience, UserBlogPage, Report,
    Passkey, AppAttackReport, PenTestingRequest, SecureCodeReviewRequest
)


class Command(BaseCommand):
    help = 'Generate dummy data for all admin panel models'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting dummy data generation...'))
        
        # Generate Users first (needed for foreign key relationships)
        self.create_users()
        
        # Generate other models
        self.create_admin_notifications()
        self.create_api_models()
        self.create_webpages()
        self.create_projects()
        self.create_courses()
        self.create_skills()
        self.create_students()
        self.create_contacts()
        self.create_ddt_contacts()
        self.create_progress()
        self.create_articles()
        self.create_smishing_join_us()
        self.create_projects_join_us()
        self.create_profiles()
        self.create_cyber_challenges()
        self.create_user_challenges()
        self.create_blog_posts()
        self.create_announcements()
        self.create_security_events()
        self.create_example_models()
        self.create_contact_submissions()
        self.create_jobs()
        self.create_job_applications()
        self.create_leaderboard_tables()
        self.create_experiences()
        self.create_user_blog_pages()
        self.create_reports()
        self.create_passkeys()
        self.create_appattack_reports()
        self.create_pen_testing_requests()
        self.create_secure_code_review_requests()
        
        self.stdout.write(self.style.SUCCESS('Dummy data generation completed!'))

    def create_users(self):
        self.stdout.write('Creating Users...')
        for i in range(1, 4):
            User.objects.get_or_create(
                email=f'user{i}@deakin.edu.au',
                defaults={
                    'first_name': f'User{i}',
                    'last_name': f'Test{i}',
                    'is_active': True,
                    'is_verified': True,
                    'upskilling_progress': {'skill1': 50, 'skill2': 75}
                }
            )

    def create_admin_notifications(self):
        self.stdout.write('Creating AdminNotifications...')
        users = User.objects.all()
        types = ['feedback', 'update', 'alert', 'info']
        for i in range(1, 4):
            AdminNotification.objects.get_or_create(
                title=f'Admin Notification {i}',
                defaults={
                    'message': f'This is admin notification message {i}',
                    'notification_type': types[i % len(types)],
                    'is_read': i % 2 == 0,
                    'related_user': users[i % len(users)] if users else None
                }
            )

    def create_api_models(self):
        self.stdout.write('Creating APIModels...')
        for i in range(1, 4):
            APIModel.objects.get_or_create(
                name=f'API Model {i}',
                defaults={
                    'field_name': f'field_name_{i}',
                    'description': f'Description for API Model {i}'
                }
            )

    def create_webpages(self):
        self.stdout.write('Creating Webpages...')
        for i in range(1, 4):
            Webpage.objects.get_or_create(
                url=f'/page{i}/',
                defaults={
                    'title': f'Test Page {i}'
                }
            )

    def create_projects(self):
        self.stdout.write('Creating Projects...')
        choices = ['AppAttack', 'Malware', 'PT-GUI']
        for i, choice in enumerate(choices, 1):
            Project.objects.get_or_create(
                title=choice,
                defaults={
                    'created_at': timezone.now(),
                    'updated_at': timezone.now()
                }
            )

    def create_courses(self):
        self.stdout.write('Creating Courses...')
        for i in range(1, 4):
            Course.objects.get_or_create(
                title=f'Course {i}',
                defaults={
                    'code': f'SIT{780 + i}',
                    'is_postgraduate': i % 2 == 0,
                    'created_at': timezone.now(),
                    'updated_at': timezone.now()
                }
            )

    def create_skills(self):
        self.stdout.write('Creating Skills...')
        skills = ['Python Programming', 'Web Security', 'Network Analysis']
        for i, skill_name in enumerate(skills, 1):
            Skill.objects.get_or_create(
                name=skill_name,
                defaults={
                    'description': f'Description for {skill_name}',
                    'slug': skill_name.lower().replace(' ', '-')
                }
            )

    def create_students(self):
        self.stdout.write('Creating Students...')
        users = User.objects.all()
        projects = Project.objects.all()
        courses = ['BCS', 'BIT', 'BCYB']
        units = ['SIT782', 'SIT764', 'SIT378']
        
        for i in range(1, 4):
            if i-1 < len(users) and projects.count() >= 3:
                Student.objects.get_or_create(
                    id=220000000 + i,
                    defaults={
                        'user': users[i-1],
                        'year': 2024,
                        'trimester': 'T1',
                        'unit': units[i-1],
                        'course': courses[i-1],
                        'p1': projects[0],
                        'p2': projects[1] if projects.count() > 1 else None,
                        'p3': projects[2] if projects.count() > 2 else None,
                        'allocated': projects[i % len(projects)],
                        'created_at': timezone.now(),
                        'updated_at': timezone.now()
                    }
                )

    def create_contacts(self):
        self.stdout.write('Creating Contacts...')
        for i in range(1, 4):
            Contact.objects.get_or_create(
                email=f'contact{i}@example.com',
                defaults={
                    'name': f'Contact Person {i}',
                    'message': f'Contact message {i}'
                }
            )

    def create_ddt_contacts(self):
        self.stdout.write('Creating DDT Contacts...')
        for i in range(1, 4):
            DDT_contact.objects.get_or_create(
                email=f'ddt{i}@example.com',
                defaults={
                    'fullname': f'DDT Contact {i}',
                    'mobile': f'04{i}123456{i}',
                    'message': f'DDT contact message {i}'
                }
            )

    def create_progress(self):
        self.stdout.write('Creating Progress...')
        students = Student.objects.all()
        skills = Skill.objects.all()
        
        if students and skills:
            for i, student in enumerate(students):
                for j, skill in enumerate(skills):
                    Progress.objects.get_or_create(
                        student=student,
                        skill=skill,
                        defaults={
                            'progress': (i + j + 1) * 20,
                            'completed': (i + j) % 2 == 0
                        }
                    )

    def create_articles(self):
        self.stdout.write('Creating Articles...')
        users = User.objects.all()
        for i in range(1, 4):
            if users:
                Article.objects.get_or_create(
                    title=f'Article {i}',
                    defaults={
                        'content': f'<p>Content for article {i}</p>',
                        'author': users[i % len(users)],
                        'featured': i % 2 == 0
                    }
                )

    def create_smishing_join_us(self):
        self.stdout.write('Creating Smishing Join Us...')
        for i in range(1, 4):
            Smishingdetection_join_us.objects.get_or_create(
                email=f'smishing{i}@example.com',
                defaults={
                    'name': f'Smishing User {i}',
                    'message': f'Smishing join message {i}'
                }
            )

    def create_projects_join_us(self):
        self.stdout.write('Creating Projects Join Us...')
        for i in range(1, 4):
            Projects_join_us.objects.get_or_create(
                email=f'project{i}@example.com',
                defaults={
                    'name': f'Project User {i}',
                    'message': f'Project join message {i}',
                    'page_name': f'Page {i}'
                }
            )

    def create_profiles(self):
        self.stdout.write('Creating Profiles...')
        users = User.objects.all()
        for i, user in enumerate(users, 1):
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'Bio for user {i}',
                    'linkedin': f'https://linkedin.com/in/user{i}',
                    'github': f'https://github.com/user{i}',
                    'location': f'City {i}'
                }
            )

    def create_cyber_challenges(self):
        self.stdout.write('Creating Cyber Challenges...')
        difficulties = ['easy', 'medium', 'hard']
        categories = ['network', 'web', 'crypto']
        types = ['mcq', 'fix_code']
        
        for i in range(1, 4):
            CyberChallenge.objects.get_or_create(
                title=f'Cyber Challenge {i}',
                defaults={
                    'description': f'Description for challenge {i}',
                    'question': f'Question for challenge {i}',
                    'choices': {'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
                    'correct_answer': 'A',
                    'explanation': f'Explanation for challenge {i}',
                    'difficulty': difficulties[i-1],
                    'category': categories[i-1],
                    'points': i * 10,
                    'challenge_type': types[i % len(types)],
                    'time_limit': 60 + (i * 30)
                }
            )

    def create_user_challenges(self):
        self.stdout.write('Creating User Challenges...')
        users = User.objects.all()
        challenges = CyberChallenge.objects.all()
        
        if users and challenges:
            for i, user in enumerate(users):
                for j, challenge in enumerate(challenges):
                    UserChallenge.objects.get_or_create(
                        user=user,
                        challenge=challenge,
                        defaults={
                            'completed': (i + j) % 2 == 0,
                            'score': (i + j + 1) * 20
                        }
                    )

    def create_blog_posts(self):
        self.stdout.write('Creating Blog Posts...')
        for i in range(1, 4):
            BlogPost.objects.get_or_create(
                title=f'Blog Post {i}',
                defaults={
                    'body': f'Body content for blog post {i}',
                    'page_name': f'page_{i}'
                }
            )

    def create_announcements(self):
        self.stdout.write('Creating Announcements...')
        for i in range(1, 4):
            Announcement.objects.get_or_create(
                message=f'Announcement message {i}',
                defaults={
                    'isActive': i % 2 == 1
                }
            )

    def create_security_events(self):
        self.stdout.write('Creating Security Events...')
        users = User.objects.all()
        events = ['login_success', 'login_failure', 'password_change']
        
        for i in range(1, 4):
            SecurityEvent.objects.get_or_create(
                event_type=events[i-1],
                ip_address=f'192.168.1.{i}',
                defaults={
                    'user': users[i % len(users)] if users else None,
                    'details': f'Details for security event {i}'
                }
            )

    def create_example_models(self):
        self.stdout.write('Creating Example Models...')
        for i in range(1, 4):
            ExampleModel.objects.get_or_create(
                name=f'Example Model {i}'
            )

    def create_contact_submissions(self):
        self.stdout.write('Creating Contact Submissions...')
        for i in range(1, 4):
            ContactSubmission.objects.get_or_create(
                email=f'submission{i}@example.com',
                defaults={
                    'first_name': f'First{i}',
                    'last_name': f'Last{i}',
                    'message': f'Contact submission message {i}'
                }
            )

    def create_jobs(self):
        self.stdout.write('Creating Jobs...')
        job_types = ['FT', 'PT', 'CT']
        locations = ['Remote', 'OnSite']
        
        for i in range(1, 4):
            Job.objects.get_or_create(
                title=f'Job Title {i}',
                defaults={
                    'description': f'<p>Job description {i}</p>',
                    'location': locations[i % len(locations)],
                    'job_type': job_types[i-1],
                    'closing_date': timezone.now().date() + timedelta(days=30)
                }
            )

    def create_job_applications(self):
        self.stdout.write('Creating Job Applications...')
        jobs = Job.objects.all()
        
        for i in range(1, 4):
            if jobs:
                JobApplication.objects.get_or_create(
                    email=f'applicant{i}@example.com',
                    job=jobs[i % len(jobs)],
                    defaults={
                        'name': f'Applicant {i}'
                    }
                )

    def create_leaderboard_tables(self):
        self.stdout.write('Creating Leaderboard Tables...')
        users = User.objects.all()
        categories = ['Web Security', 'Network Security', 'Cryptography']
        
        for i, user in enumerate(users):
            LeaderBoardTable.objects.get_or_create(
                user=user,
                category=categories[i % len(categories)],
                defaults={
                    'total_points': (i + 1) * 100
                }
            )

    def create_experiences(self):
        self.stdout.write('Creating Experiences...')
        for i in range(1, 4):
            Experience.objects.get_or_create(
                name=f'Experience User {i}',
                defaults={
                    'feedback': f'Experience feedback {i}',
                    'rating': i + 2
                }
            )

    def create_user_blog_pages(self):
        self.stdout.write('Creating User Blog Pages...')
        for i in range(1, 4):
            UserBlogPage.objects.get_or_create(
                name=f'Blog User {i}',
                defaults={
                    'title': f'Blog Title {i}',
                    'description': f'Blog description {i}',
                    'file': '',
                    'isShow': i % 2 == 1
                }
            )

    def create_reports(self):
        self.stdout.write('Creating Reports...')
        for i in range(1, 4):
            Report.objects.get_or_create(
                blog_id=i,
                defaults={
                    'blog_name': f'Blog Name {i}',
                    'reason': f'Report reason {i}'
                }
            )

    def create_passkeys(self):
        self.stdout.write('Creating Passkeys...')
        users = User.objects.all()
        
        for i, user in enumerate(users, 1):
            for j in range(3):  # Create 3 passkeys per user
                Passkey.objects.get_or_create(
                    user=user,
                    key=f'PASS{i}{j}ABCDEF',
                    defaults={}
                )

    def create_appattack_reports(self):
        self.stdout.write('Creating AppAttack Reports...')
        for i in range(1, 4):
            AppAttackReport.objects.get_or_create(
                year=2024 + i - 1,
                title=f'AppAttack Report {i}',
                defaults={}
            )

    def create_pen_testing_requests(self):
        self.stdout.write('Creating Pen Testing Requests...')
        for i in range(1, 4):
            PenTestingRequest.objects.get_or_create(
                email=f'pentest{i}@example.com',
                defaults={
                    'name': f'PenTest User {i}',
                    'github_repo_link': f'https://github.com/user{i}/repo{i}',
                    'project_description': f'Project description {i}',
                    'terms_accepted': True
                }
            )

    def create_secure_code_review_requests(self):
        self.stdout.write('Creating Secure Code Review Requests...')
        for i in range(1, 4):
            SecureCodeReviewRequest.objects.get_or_create(
                email=f'codereview{i}@example.com',
                defaults={
                    'name': f'CodeReview User {i}',
                    'github_repo_link': f'https://github.com/user{i}/security{i}',
                    'project_description': f'Security review description {i}',
                    'terms_accepted': True
                }
            ) 