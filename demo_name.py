# Copyright [yyyy] [name of copyright owner]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Things to do:
 - Please name this file <demo_name>.py
 - Fill in [yyyy] and [name of copyright owner] in the copyright (top line)
 - Add demo code below
 - Format code so that it conforms with PEP 8
"""

from dimod import ConstrainedQuadraticModel, Binary
from dwave.system import LeapHybridCQMSampler
from itertools import product


#Consts
vehicles = [f'v{n}' for n in range(1, 4)]
destinations = ['0'] + [f'{dir}{n}' for dir in ['NE', 'NW', 'SW', 'SE'] for n in range(1, 4)]
times = {}
for element in product(destinations, destinations):
    q, p = element
    if q == p:
        times[element] = 0
    elif q == "0" and p != "0":
        # Transition from depot to node is cheap.
        times[element] = int(p[-1])  # or another low cost value
    # elif p == "0" and q != "0":
    #     # Transition from node to depot is expensive.
    #     times[element] = 9999999  # high penalty
    else:
        # For node-to-node transitions, apply your logic.
        if q[:-1] == p[:-1]:  # comparing the directional part (assuming format like 'NE1')
            times[element] = int(q[-1]) + int(p[-1])
        else:
            times[element] = 20

gas_cap = 250
time_cap = 250
num_vehicles = 3
efficiency_constant = 0.05
intensity_inverse = {}
intensity_inverse['0'] = 9999999
for i in range(1, len(destinations)):
    intensity_inverse[destinations[i]] = i

#variables

d = {(i,j):Binary(f'd_{i}{j}') for i in vehicles for j in destinations}
'''list_test = []
for a in vehicles:
    for b in destinations:
        for c in destinations:
            list_test.append(d[(a, b)]*d[(a, c)]*times[(b, c)]*intensity_inverse[c])'''

#x = dimod.Binary((1, 2))
#x = [Binary(f'x_{i}')]
#does x[1] == 2?

#instantiate model
cqm = ConstrainedQuadraticModel()
# cqm.set_objective(sum(d[(a, b)]*d[(a, c)]*times[(b, c)]*intensity_inverse[c]) for a in vehicles for b in destinations for c in destinations)

cqm.set_objective(sum(d[(a, b)]*d[(a, c)]*times[(b, c)]*intensity_inverse[c] for a in vehicles for b in destinations for c in destinations[1:]))

#cqm.set_objective(sum(list_test))
for j in destinations:
    cqm.add_constraint(sum(d[a, j] for a in vehicles) <= num_vehicles)
for i in vehicles:
    cqm.add_constraint(efficiency_constant*sum(d[i, b]*d[i, c]*times[b, c] for b in destinations for c in destinations[1:]) >= 0)
    cqm.add_constraint(efficiency_constant*sum(d[i, b]*d[i, c]*times[b, c] for b in destinations for c in destinations[1:]) <= gas_cap)
for i in vehicles:
    cqm.add_constraint(sum(d[i, b]*d[i, c]*times[b, c] for b in destinations for c in destinations[1:]) >= 0)
    cqm.add_constraint(sum(d[i, b]*d[i, c]*times[b, c] for b in destinations for c in destinations[1:]) <= time_cap)
for i in vehicles:
    cqm.add_constraint(d[i, '0']==1)
for j in destinations[1:]:
    cqm.add_constraint(sum(d[a, j] for a in vehicles) >= 1)

#add constraints

#set objective

#instantiate solver
sampler = LeapHybridCQMSampler()
sample_set = sampler.sample_cqm(cqm, time_limit=15)
feasible_samples = sample_set.filter(lambda d: d.is_feasible)
best_result = feasible_samples.first
print(best_result)
#submit sample set

#filter results

#return top results