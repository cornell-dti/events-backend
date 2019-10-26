from app.models import Tag
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Adds tags to the database'

    """
    Right now doesn't take any args
    What is a good way to pass in args?
    Strings representing start/end dates? (Ex: '2019-10-06')
    """

    def handle(self, *args, **kwargs):
        tags = [
            'Free-Food',
            'Career',
            'Social',
            'Athletic',
            'Other',
            'Outdoors',
            'Academic',
            'Professional',
            'Entrepreneurship',
            'Engineering',
            'Hotel',
            'ILR',
            'Hum-Ec',
            'Aap',
            'CALS',
            'A&S',
            'Design',
            'Business',
            'Acapella',
            'Jazz',
            'Government',
            'Art',
            'Tech',
            'Philanthropy',
            'Networking',
            'Speaker',
            'Alumni',
            'Comedy',
            'Astronomy',
            'Biology',
            'Music',
            'Language',
            'Theater',
            'Dance',
            'Consulting',
            'Investing',
            'Political',
            'Religion',
            'Greek-Life',
            'Environment',
            'Outdoors',
            'Varsity-Sports',
            'Sports',
            'Concert',
            'Health',
            'Cultural',
            'Project-Team',
            'Finance',
            'Graduate',
            'Law',
            'Fashion',
            'Sustainability',
            'Education',
            'Medical',
            'Publication',
            'Student-Government',
            'Debate',
            'Gaming',
            'Kid-Friendly',
            'Nightlife',
            'Leadership',
            'International',
            'Info-Session',
            'Interview-Prep',
            'Recruitment',
            'Mental-Health',
            'Workshop',
            'Fundraiser',
            'Career-Fair',
            'Hackathon',
            'Lecture',
            'Exhibition',
            'Bake-Sale',
            'Corporate',
            'Mentorship',
        ]
        for tag in tags:
            tag_obj = Tag(name=tag)
            tag_obj.save()
