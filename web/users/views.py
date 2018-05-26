from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from . import forms
from django.views.generic import FormView, RedirectView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('home')

    def get(self, request):
        login_form = forms.LoginForm()
        register_form = forms.RegisterForm()
        next_string = '?next={}'.format(request.GET['next']) if 'next' in request.GET else ''
        ctx = {
            'login_form': login_form,
            'register_form': register_form,
            'next_string': next_string
        }
        return render(request, self.template_name, ctx)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

        if user:
            login(self.request, user)
            redirect_to = self.request.GET['next'] if 'next' in self.request.GET else 'home'
            return redirect(redirect_to)

        register_form = forms.RegisterForm()
        ctx = {'login_form': form, 'register_form': register_form}
        return render(self.request, self.template_name, ctx)

    def form_invalid(self, form):
        context = self.get_context_data(login_form=form, register_form=forms.RegisterForm)
        return self.render_to_response(context)


class RegisterView(FormView):
    template_name = 'users/login.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy('users:login')

    def get(self, request):
        return redirect('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.add_message(self.request, messages.INFO, 'You are successfully registered!')
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(register_form=form, login_form=forms.LoginForm)
        return self.render_to_response(context)


class LogoutView(RedirectView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('home'))
