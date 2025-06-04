from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from studentorg.forms import (
    CollegeForm,
    OrganizationForm,
    OrgMembersForm,
    ProgramForm,
    StudentsForm,
)
from studentorg.models import Boat, College, Organization, OrgMember, Program, Student


#for chartAdd commentMore actions
import json

from django.db.models import Count
from .models import Student,Program, College, Organization, OrgMember
from django.db.models.functions import TruncYear

"""
def chart_view(request):
    # College chart
    colleges = College.objects.annotate(total=Count('program__student')).order_by('college_name')
    college_names = [college.college_name for college in colleges]
    student_counts = [college.total for college in colleges]

    # Program chart
    programs = Program.objects.annotate(student_count=Count('student')).order_by('-student_count')
    program_names = [program.prog_name for program in programs]
    program_counts = [program.student_count for program in programs]

    # Students per Organization chart (new)
    organizations = Organization.objects.annotate(student_count=Count('orgmember')).order_by('name')
    org_names = [org.name for org in organizations]
    org_student_counts = [org.student_count for org in organizations]

    context = {
        'college_names': json.dumps(college_names),
        'student_counts': json.dumps(student_counts),
        'program_names': json.dumps(program_names),
        'program_counts': json.dumps(program_counts),
        'org_names': json.dumps(org_names),
        'org_student_counts': json.dumps(org_student_counts),
    }

    return render(request, 'chart.html', context)
"""

from django.db.models import Count
import json

def chart_view(request):
    # College chart: Number of students per college
    colleges = College.objects.annotate(total=Count('program__student')).order_by('college_name')
    college_names = [college.college_name for college in colleges]
    student_counts = [college.total for college in colleges]

    # Program chart: Top programs by number of students
    programs = Program.objects.annotate(student_count=Count('student')).order_by('-student_count')
    program_names = [program.prog_name for program in programs]
    program_counts = [program.student_count for program in programs]

    # Top 5 Organizations by Number of Student Members (Bar Chart)
    top_organizations = Organization.objects.annotate(student_count=Count('orgmember')).order_by('-student_count')[:5]
    org_names = [org.name for org in top_organizations]
    org_student_counts = [org.student_count for org in top_organizations]

    # Student Enrollment Over Time chart (by year)
    student_enrollment_by_year = Student.objects.annotate(
        year=TruncYear('created_at')
    ).values('year').annotate(
        total=Count('id')
    ).order_by('year')

    college_years = [entry['year'].year for entry in student_enrollment_by_year]
    counts_by_year = [entry['total'] for entry in student_enrollment_by_year]

    context = {
        'college_names': json.dumps(college_names),
        'student_counts': json.dumps(student_counts),
        'program_names': json.dumps(program_names),
        'program_counts': json.dumps(program_counts),
        'org_names': json.dumps(org_names),
        'org_student_counts': json.dumps(org_student_counts),
        'college_years': json.dumps(college_years),
        'counts_by_year': json.dumps(counts_by_year),
    }

    return render(request, 'chart.html', context)

# Create your views here.


class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

# Organization List View


class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = "org_list.html"
    paginate_by = 5


class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Organization "{form.instance.name}" has been successfully created.'
        )
        return super().form_valid(form)


class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Organization "{form.instance.name}" has been successfully updated.'
        )
        return super().form_valid(form)


class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

    def form_valid(self, form):
        organization = self.get_object()
        messages.success(
            self.request,
            f'Organization "{organization.name}" has been successfully deleted.'
        )
        return super().form_valid(form)

# Org Member List View


class OrgMembersList(ListView):
    model = OrgMember
    context_object_name = 'org_member'
    template_name = "org_members_list.html"
    paginate_by = 5


class OrgMembersCreateView(CreateView):
    model = OrgMember
    form_class = OrgMembersForm
    template_name = 'org_members_add.html'
    success_url = reverse_lazy('org-members-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Organization member "{form.instance.student}" has been successfully created.'
        )
        return super().form_valid(form)


class OrgMembersUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMembersForm
    template_name = 'org_members_edit.html'
    success_url = reverse_lazy('org-members-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Organization member "{form.instance.student}" has been successfully updated.'
        )
        return super().form_valid(form)


class OrgMembersDeleteView(DeleteView):
    model = OrgMember
    template_name = 'org_members_del.html'
    success_url = reverse_lazy('org-members-list')

    def form_valid(self, form):
        org_member = self.get_object()
        messages.success(
            self.request,
            f'Organization member "{org_member.student}" has been successfully deleted.'
        )
        return super().form_valid(form)


# Students List View


class StudentsList(ListView):
    model = Student
    context_object_name = 'students'
    template_name = "students_list.html"
    paginate_by = 5


class StudentsCreateView(CreateView):
    model = Student
    form_class = StudentsForm
    template_name = 'students_add.html'
    success_url = reverse_lazy('students-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Student "{form.instance}" has been successfully created.'
        )
        return super().form_valid(form)


class StudentsUpdateView(UpdateView):
    model = Student
    form_class = StudentsForm
    template_name = 'students_edit.html'
    success_url = reverse_lazy('students-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Student "{form.instance}" has been successfully updated.'
        )
        return super().form_valid(form)


class StudentsDeleteView(DeleteView):
    model = Student
    template_name = 'students_del.html'
    success_url = reverse_lazy('students-list')

    def form_valid(self, form):
        student = self.get_object()
        messages.success(
            self.request,
            f'Student "{student}" has been successfully deleted.'
        )
        return super().form_valid(form)


# College List View


class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = "college_list.html"
    paginate_by = 5


class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'College "{form.instance.college_name}" has been successfully created.'
        )
        return super().form_valid(form)


class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

    def form_valid(self, form):
        college_name = form.instance.college_name
        messages.success(self.request, f'College "{college_name}" has been successfully updated.')

        return super().form_valid(form)


class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')

    def form_valid(self, form):
        college = self.get_object()
        messages.success(
            self.request,
            f'College "{college.college_name}" has been successfully deleted.'
        )
        return super().form_valid(form)


# Program List View


class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = "program_list.html"
    paginate_by = 5


class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')

    def form_valid(self, form):
        prog_name = form.instance.prog_name
        messages.success(
            self.request,
            f'Program "{prog_name}" has been successfully created.'
        )
        return super().form_valid(form)


class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')

    def form_valid(self, form):
        prog_name = form.instance.prog_name
        messages.success(
            self.request,
            f'Program "{prog_name}" has been successfully updated.'
        )
        return super().form_valid(form)


class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')

    def form_valid(self, form):
        program = self.get_object()
        messages.success(
            self.request,
            f'Program "{program.prog_name}" has been successfully deleted.'
        )
        return super().form_valid(form)


class BoatCreateView(CreateView):
    model = Boat
    fields = "__all__"
    template_name = 'boat_form.html'
    success_url = reverse_lazy('boat-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Boat "{form.instance.name}" has been successfully created.'
        )
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        length = request.POST.get('length')
        width = request.POST.get('width')
        height = request.POST.get('height')

        # Validate the dimensions
        errors = []
        for field_name, value in [
            ('length', length),
            ('width', width),
            ('height', height)
        ]:
            try:
                if float(value) <= 0:
                    errors.append(
                        f"{field_name.capitalize()} must be greater than 0."
                    )
            except (ValueError, TypeError):
                errors.append(
                    f"{field_name.capitalize()} must be a valid number."
                )

        # if errors exist, display them and return to the form
        if errors:
            for error in errors:
                messages.error(request, error)
            return self.form_invalid(self.get_form())

        # Call the parent post() if validation passes
        return super().post(request, *args, **kwargs)


class BoatUpdateView(UpdateView):
    model = Boat
    fields = "__all__"
    template_name = 'boat_form.html'
    success_url = reverse_lazy('boat-list')

    def form_valid(self, form):
        messages.success(
            self.request,
            f'Boat "{form.instance.name}" has been successfully updated.'
        )
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        length = request.POST.get('length')
        width = request.POST.get('width')
        height = request.POST.get('height')

        # Validate dimensions
        errors = []
        for field_name, value in [
            ('length', length),
            ('width', width),
            ('height', height)
        ]:
            try:
                if float(value) <= 0:
                    errors.append(
                        f"{field_name.capitalize()} must be greater than 0."
                    )
            except (ValueError, TypeError):
                errors.append(
                    f"{field_name.capitalize()} must be a valid number."
                )

        # if errors exist, display them and return to the form
        if errors:
            for error in errors:
                messages.error(request, error)
            return self.form_invalid(self.get_form())

        # Call the parent post() if validation passes
        return super().post(request, *args, **kwargs)
