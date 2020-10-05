import datetime

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from catalog.models import Book, BookInstance, Author
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from catalog.forms import RenewBookModelForms


def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForms(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForms(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


def index(request):
    num_book = Book.objects.count()
    num_instance = BookInstance.objects.count()
    num_instance_available = BookInstance.objects.filter(status__exact='m').count()
    num_author = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    num_visits = num_visits + 1
    request.session['num_visits'] = num_visits

    messages.info(request, 'Hello world test')
    messages.success(request, 'Your information was sent successfully!')

    context = {'num_book': num_book, 'num_instance': num_instance, 'num_instances_available': num_instance_available,
               'num_authors': num_author, 'num_visits': num_visits}

    return render(request, 'index.html', context=context)


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    success_url = reverse_lazy('authors')


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    success_url = reverse_lazy('authors')


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 2

    def get_queryset(self):
        return Book.objects.filter()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(SuccessMessageMixin, generic.ListView):
    model = Author
    paginate_by = 2

    success_message = "this is a testmessage"


class AuthorDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Author
    permission_required = 'catalog.can_mark_returned'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 2
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).order_by('due_back')


class BorrowedBooksListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/bookinstance_list_borrowed.html'

    def get_queryset(self):
        return BookInstance.objects.exclude(borrower__isnull=True).order_by('due_back')
