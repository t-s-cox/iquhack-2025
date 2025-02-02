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
from random import random
from random import seed

#SEED
seed(1)

#CONSTS
gas_cap = 500
time_cap = 500
num_vehicles = 1
num_destinations = 8
efficiency_constant = 0.05

#VAR ARRAYS
vehicles = [f'v{n}' for n in range(1, num_vehicles+1)]
destinations = [0] + [m in range(1, num_destinations+1)]
times = {}
for element in product(destinations, destinations):
    q, p = element
    if q == p:
        times[element] = 0
    else:
        times[element] = floor(900*random() + 100)


times[0, 1] = 2
times[1, 2] = 4
times[2, 3] = 6
times[3, 4] = 8
times[4, 5] = 5
times[5, 6] = 5
times[6, 7] = 4
times[7, 0] = 5
times[0, 4] = 6

#VARS
d = {(i,j):Binary(f'd_{i}{j}') for i in vehicles for j in destinations}

intensity_inverse = {}
intensity_inverse['0'] = 1000
for i in range(1, len(destinations)):
    intensity_inverse[destinations[i]] = 1


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
    cqm.add_constraint(d[i, 0]==1)
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