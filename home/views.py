import requests, pulp, openrouteservice, numpy as np
from .forms import UserLoginForm, LocationCreateEditForm, SessionCreateEditForm, UserRegistrationForm, CustomerEditForm, CustomerCreateForm
from .models import Location, Session, Customer
from .functions import neshan_distance_matrix, neshan_cor_addr, ping
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from requests.exceptions import RequestException
# Create your views here.





class HomeView(LoginRequiredMixin, View):
    

    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        customers = Customer.objects.all()
        sessions = Session.objects.all()

        if ping() == 1:
            messages.warning(request, '''Couldn't ping the services! Check Your Internet.''', 'warning')

        return render(request, 'home/index.html', {'locations':locations, 'sessions': sessions, 'customers':customers})
    

class LoginView(View):
    form_class = UserLoginForm


    def dispatch(self, request, *args, **kwargs):
        # if ping() == 1:
        #     messages.warning(request, '''Couldn't ping the services! Check Your Internet.''', 'warning')
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/login.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {user.username}!', 'success')
                return redirect('home:home')
            messages.error(request, 'Username or Password is WRONG', 'warning')
        return render(request, 'home/login.html', {'form': form})
    

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        urname = request.user.username
        logout(request)
        messages.success(request, f'Come Back Soon, {urname}', 'success')
        return redirect('home:home')
    

class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'home/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, f'Registered Successfully. Enjoy {cd['username']}!', 'success')
            return redirect('home:user_login')
        return render(request, self.template_name, {'form':form})

class AddLocationView(LoginRequiredMixin, PermissionRequiredMixin, View):
    class_form = LocationCreateEditForm
    permission_required = 'home.add_location'
    
    def dispatch(self, request, *args, **kwargs):
        if ping() == 1:
            messages.warning(request, '''Couldn't ping the services! Check Your Internet.''', 'warning')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.class_form()
        return render(request, 'home/add_location.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            latitude = cd['lat_lon'].split(', ')[0]
            longitude = cd['lat_lon'].split(', ')[1]
            try:
                Location.objects.create(name=name, latitude=latitude, longitude=longitude)
                messages.success(request, f'{name} created successfully!')
                form = self.class_form()
            except ValueError:
                messages.error(request, 'Invalid Input', 'danger')    
        return render(request, 'home/add_location.html', {'form':form}) 
    

class AddCustomerView(LoginRequiredMixin, View):
    class_form = CustomerCreateForm
    class_template = 'home/add_customer.html'

    def dispatch(self, request, *args, **kwargs):
        if ping() == 1:
            messages.warning(request, '''Couldn't ping the services! Check Your Internet.''', 'warning')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = self.class_form()
        return render(request, self.class_template, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            latitude = cd['lat_lon'].split(', ')[0]
            longitude = cd['lat_lon'].split(', ')[1]
            shop_name = cd['shop_name']
            try:
                address = neshan_cor_addr(lat=latitude, lon=longitude)
            except requests.exceptions.RequestException:
                address = 'Null'
                messages.error(request, '''Due to connection Failure, default address set to 'Null'! ''', 'danger')
            try:
                Customer.objects.create(name=name, latitude=latitude, longitude=longitude, shop_name=shop_name, address=address)
                messages.success(request, f'{name} created successfully!')
                form = self.class_form()
            except ValueError:
                messages.error(request, 'Invalid Input', 'danger')    
        return render(request, self.class_template, {'form':form}) 
 

class CustomerDetailView(View):
    def get(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=kwargs['customer_id'])
        for_map = []
        for_map_lib = {}
        for_map_lib['name'] = customer.name
        for_map_lib['lat'] = customer.latitude
        for_map_lib['lng'] = customer.longitude
        for_map.append(for_map_lib)

        return render(request, 'home/customer_detail.html', {'customer': customer, 'for_map': for_map})


class CustomerEditView(View):
    class_form = CustomerEditForm
    class_template = 'home/customer_edit.html'

    def setup(self, request, *args, **kwargs):
        self.customer_instance = Customer.objects.get(pk=kwargs['customer_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        customer = self.customer_instance
        form = self.class_form(instance=customer)
        return render(request, self.class_template, {'form': form, 'customer': customer})
    
    def post(self, request, *args, **kwargs):
        customer = self.customer_instance
        form = self.class_form(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer Edited Successfully!', 'success')
            return redirect('home:customer_detail', customer.id)
        messages.error(request, 'Invalid Input!', 'danger')
        return redirect('home:customer_detail', customer.id)


class LocationDetailView(View):
    def get(self, request, *args, **kwargs):
        loc = Location.objects.get(pk=kwargs['location_id'])
        for_map = []
        for_map_lib = {}
        for_map_lib['name'] = loc.name
        for_map_lib['lat'] = loc.latitude
        for_map_lib['lng'] = loc.longitude
        for_map.append(for_map_lib)

        if ping('8.8.8.8') == 1:
            messages.warning(request, '''Couldn't ping the services! Check Your Internet.''', 'warning')

        return render(request, 'home/location_detail.html', {'loc': loc, 'for_map': for_map})
    

class LocationListView(View):
    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        return render(request, 'home/location_list.html', {'locations': locations})


class SessionListView(View):
    def get(self, request, *args, **kwargs):
        sessions = Session.objects.all()
        return render(request, 'home/location_list.html', {'sessions': sessions})


class CustomerListView(View):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        return render(request, 'home/location_list.html', {'customers': customers})


class LocationDeleteView(View):

    def get(self, request, *args, **kwargs):
        location = Location.objects.get(pk=kwargs['location_id'])
        location_name = location.name
        location.delete()
        messages.success(request, f'''Location "{location_name}" deleted successfully!''', 'success')
        return redirect('home:home')


class AddSessionView(LoginRequiredMixin, View):
    class_form = SessionCreateEditForm
    def get(self, request, *args, **kwargs):
        form = self.class_form()
        return render(request, 'home/add_session.html', {'form': form})
    
    def post(self, request, *args, **kwargs0):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            form.save()
            messages.success(request, f'{name} added to sessions')
        return redirect('home:home')
    

class SessionDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        session = Session.objects.get(pk=kwargs['session_id'])
        customers = session.customer.all()
        return render(request, 'home/session_detail.html', {'session': session, 'customers':customers})
    

class SessionEditView(LoginRequiredMixin, View):
    class_form = SessionCreateEditForm

    def setup(self, request, *args, **kwargs):
        self.session_instance = Session.objects.get(pk=kwargs['session_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session = self.session_instance
        form = self.class_form(instance=session)
        return render(request, 'home/session_edit.html', {'form': form, 'session':session})
    
    def post(self, request, *args, **kwargs):
        session = self.session_instance
        form = self.class_form(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Session Edited Successfully!', 'success')
            return redirect('home:session_detail', session.id)
        messages.error(request, 'Invalid Input!', 'danger')
        return redirect('home:session_detail', session.id)


class SessionDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        session = Session.objects.get(pk = kwargs['session_id'])
        session.delete()
        messages.success(request, 'Session Deleted Successfully!', 'success')
        return redirect('home:home')


class SessionCalculationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if ping() == 0:
            location_list = []
            inventory = get_object_or_404(Location, name='Inventory')
            session = Session.objects.get(pk=kwargs['session_id'])
            locations = session.customer.all()

            # The following section will return the needed string format for Neshan Api
            string = str(inventory.latitude) + ',' + str(inventory.longitude)

            list = []
            for_map = [{'name': inventory.name, 'lat': inventory.latitude, 'lng': inventory.longitude}]
            for c in locations:
                this_location = {}
                lat = c.latitude
                lon = c.longitude
                this_string = f'{lat},{lon}'
                list.append(this_string)

                this_location['name'] = c.name
                this_location['lat'] = lat
                this_location['lng'] = lon
                for_map.append(this_location)
            
            for l in list:
                string = string + '|' + l 
            string = string[:-1]
            print(list)
            print(f'YOURS: {string}')
            # string is the desired format "END"

            distances_matrix = neshan_distance_matrix(string)
            print(distances_matrix)
            distances = np.array(distances_matrix)
            n = len(distances)

            problem = pulp.LpProblem("TSP", pulp.LpMinimize)
            x = [[pulp.LpVariable(f"x_{i}_{j}", cat=pulp.LpBinary) for j in range(n)] for i in range(n)]
            u = [pulp.LpVariable(f"u_{i}", lowBound=1, upBound=n-1, cat=pulp.LpInteger) for i in range(n)]
            try:
                problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(n) for j in range(n))
            except TypeError:
                messages.error(request, '''Couldn't Find A route due to API Malfunction.''', 'danger')
                return redirect('home:home')
            for i in range(n):
                problem += pulp.lpSum(x[i][j] for j in range(n) if j != i) == 1  
                problem += pulp.lpSum(x[j][i] for j in range(n) if j != i) == 1  

            for i in range(1, n):  
                for j in range(1, n):
                    if i != j:
                        problem += u[i] - u[j] + n * x[i][j] <= n - 1

            problem.solve()
            print(distances_matrix)
            print("Optimal Route:")
            route = {}
            next_location = {}
            position = 0
            for i in range(n):
                for j in range(n):
                    if pulp.value(x[i][j]) == 1:
                        route[position] = f"Location {i + 1} → Location {j + 1}"
                        position += 1
                        next_location[i + 1] = j + 1

            ordered_route = []
            visited = set()
            current_location = 1
            while current_location in next_location and current_location not in visited:
                visited.add(current_location)
                next_loc = next_location[current_location]
                ordered_route.append(f"Location {current_location} → Location {next_loc}")
                print(f"Location {current_location} → Location {next_loc}")
                current_location = next_loc
            
            print(f"Total Distance: {pulp.value(problem.objective)}")
            return render(request, 'home/tsp_solved.html', {'ordered_route': ordered_route, 'locations':locations, 'for_map': for_map})

        messages.error(request, 'Internet Failure! Check Your Connection', 'danger')
        return redirect('home:home')
