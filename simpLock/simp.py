import stormpy
import stormpy.info
import matplotlib.pyplot as plt
import numpy as np


prism_program = stormpy.parse_prism_program("simp.nm")
print("\n")
print(prism_program.model_type)

options = stormpy.BuilderOptions(True, True)
options.set_build_state_valuations()
options.set_build_choice_labels()
model = stormpy.stormpy.build_sparse_model_with_options(prism_program, options)

choice_labels = model.choice_labeling

number = model.nr_states
print("Number of states: {}" .format(model.nr_states))
print("Number of transitions: {}" .format(model.nr_transitions))
print("Labels: {}" .format(model.labeling.get_labels()))
print()

formula_str = 'R{\"states\"}min=? [F \"found\"]'
#formula_str = 'Pmax=? [F \"found\"]'
properties = stormpy.parse_properties(formula_str, prism_program)
#model checking
result = stormpy.model_checking(model, properties[0])

initial_state = model.states[0]
# print("Expected number of steps to reach state from initial state: ", initial_state, " -> {}" .format(result.at(initial_state)))

# print()

i=0
re = []
while(i < number):
	initial_state = model.states[i]
	# print("Expected number of steps to reach state 'found' from state: ", initial_state, " -> {}" .format(result.at(initial_state)))
	re.append(result.at(initial_state))
	i += 1


j=0
while(j < len(re)):
	if(re[j] == np.inf):
		re[j] = 0
	j += 1

plt.plot(re)
plt.xlabel('states')
plt.ylabel('steps')
plt.axis([0, number, 0, 15])
plt.legend(["steps"], loc ="upper right") 
plt.show()

#exploring model
# i=0
# while(i < number):
# 	state = model.states[i]
# 	state_vals = model.state_valuations
# 	#print(state_vals.get_string(state.id))
# 	print("\nState {} with variable values: {}" .format(state, state_vals.get_string(state.id)))
# 	choice_labels = model.choice_labeling
# 	# print()
# 	# print(choice_labels)
# 	for action in state.actions:
# 		for transition in action.transitions:
# 			print("With action {} and probability {}, go to state {} {}" .format(choice_labels.get_labels_of_choice(action.id+3), transition.value(), transition.column, state_vals.get_string(transition.column)))
# 			if transition.column > 10: break

# 	i += 1

print()