from sim_names import sim_names
import os

with open("simulation_template.html", "r") as template_file:
    sim_template = template_file.read()

for name in sim_names:
    with open("simulations/%s.html" % name, "w") as file:
        file.write(sim_template.replace("{{sim_name}}", name))

print("Done")