from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os

def index(request):
    sims = os.listdir("./phettojs/static/jars")
    sim_names = sorted(list(set(sim.replace(".jar", "").replace(".js", "") for sim in sims)))
    template = loader.get_template('phettojs/sim_list.html')
    context = {
        'sim_names': sim_names,
    }
    return HttpResponse(template.render(context, request))

def simulation(request, sim_name):
    template = loader.get_template('phettojs/simulation.html')
    context = {
        'sim_name': sim_name,
    }
    return HttpResponse(template.render(context, request))