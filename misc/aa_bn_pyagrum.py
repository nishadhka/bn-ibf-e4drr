import pyagrum as gum
import pyagrum.lib.ipython as gnb

# Create a new Bayesian network
bn = gum.BayesNet('DroughtAnticipatoryAction')

# Add variables
# Forecasted Drought Severity (FDS)
fds = bn.add(gum.LabelizedVariable('FDS', 'Forecasted Drought Severity', 2))
bn.variable(fds).addLabel('No Drought')
bn.variable(fds).addLabel('Drought')

# Observed Drought Severity (ODS)
ods = bn.add(gum.LabelizedVariable('ODS', 'Observed Drought Severity', 2))
bn.variable(ods).addLabel('No Drought')
bn.variable(ods).addLabel('Drought')

# Trigger Threshold (TT)
tt = bn.add(gum.LabelizedVariable('TT', 'Trigger Threshold', 2))
bn.variable(tt).addLabel('Not Exceeded')
bn.variable(tt).addLabel('Exceeded')

# Anticipatory Action Decision (AAD)
aad = bn.add(gum.LabelizedVariable('AAD', 'Anticipatory Action Decision', 2))
bn.variable(aad).addLabel('No Action')
bn.variable(aad).addLabel('Action Taken')

# Hit Rate (HR)
hr = bn.add(gum.LabelizedVariable('HR', 'Hit Rate', 2))
bn.variable(hr).addLabel('Low')
bn.variable(hr).addLabel('High')

# False Alarm Ratio (FAR)
far = bn.add(gum.LabelizedVariable('FAR', 'False Alarm Ratio', 2))
bn.variable(far).addLabel('High')
bn.variable(far).addLabel('Low')

# Ground Impact (GI)
gi = bn.add(gum.LabelizedVariable('GI', 'Ground Impact', 2))
bn.variable(gi).addLabel('Low Impact')
bn.variable(gi).addLabel('High Impact')

# Add arcs (dependencies)
bn.addArc(fds, aad)     # FDS influences AAD
bn.addArc(ods, hr)      # ODS and FDS influence HR
bn.addArc(fds, hr)
bn.addArc(ods, far)     # ODS and FDS influence FAR
bn.addArc(fds, far)
bn.addArc(hr, tt)       # HR influences TT
bn.addArc(far, tt)      # FAR influences TT
bn.addArc(ods, gi)      # ODS influences GI
bn.addArc(aad, gi)      # AAD influences GI

# Define Conditional Probability Tables (CPTs)

# FDS - Assume a prior probability
bn.cpt(fds).fillWith([0.7, 0.3])  # 70% chance of 'No Drought', 30% 'Drought'

# ODS - Assume historical data
bn.cpt(ods).fillWith([0.75, 0.25])  # 75% 'No Drought', 25% 'Drought'

# AAD - Depends on FDS
bn.cpt(aad)[{'FDS': 'No Drought'}] = [0.9, 0.1]  # Likely no action if no drought forecasted
bn.cpt(aad)[{'FDS': 'Drought'}] = [0.2, 0.8]     # Likely action if drought forecasted

# HR - Depends on FDS and ODS
bn.cpt(hr)[{'FDS': 'No Drought', 'ODS': 'No Drought'}] = [0.1, 0.9]
bn.cpt(hr)[{'FDS': 'No Drought', 'ODS': 'Drought'}] = [0.9, 0.1]
bn.cpt(hr)[{'FDS': 'Drought', 'ODS': 'No Drought'}] = [0.8, 0.2]
bn.cpt(hr)[{'FDS': 'Drought', 'ODS': 'Drought'}] = [0.2, 0.8]

# FAR - Depends on FDS and ODS
bn.cpt(far)[{'FDS': 'No Drought', 'ODS': 'No Drought'}] = [0.2, 0.8]
bn.cpt(far)[{'FDS': 'No Drought', 'ODS': 'Drought'}] = [0.8, 0.2]
bn.cpt(far)[{'FDS': 'Drought', 'ODS': 'No Drought'}] = [0.9, 0.1]
bn.cpt(far)[{'FDS': 'Drought', 'ODS': 'Drought'}] = [0.3, 0.7]

# TT - Depends on HR and FAR
bn.cpt(tt)[{'HR': 'Low', 'FAR': 'High'}] = [0.95, 0.05]
bn.cpt(tt)[{'HR': 'Low', 'FAR': 'Low'}] = [0.85, 0.15]
bn.cpt(tt)[{'HR': 'High', 'FAR': 'High'}] = [0.7, 0.3]
bn.cpt(tt)[{'HR': 'High', 'FAR': 'Low'}] = [0.4, 0.6]

# GI - Depends on ODS and AAD
bn.cpt(gi)[{'ODS': 'No Drought', 'AAD': 'No Action'}] = [0.95, 0.05]
bn.cpt(gi)[{'ODS': 'No Drought', 'AAD': 'Action Taken'}] = [0.9, 0.1]
bn.cpt(gi)[{'ODS': 'Drought', 'AAD': 'No Action'}] = [0.2, 0.8]
bn.cpt(gi)[{'ODS': 'Drought', 'AAD': 'Action Taken'}] = [0.6, 0.4]

# Now, we can perform inference

# Create an inference engine
ie = gum.LazyPropagation(bn)

# Set evidence if any (e.g., observed data)
# For example, let's set that the forecast predicts drought
ie.setEvidence({'FDS': 'Drought'})

# Perform inference
ie.makeInference()

# Query the posterior probabilities
print("Posterior probabilities for Anticipatory Action Decision:")
aad_posterior = ie.posterior(aad)
print(aad_posterior)

print("\nPosterior probabilities for Ground Impact:")
gi_posterior = ie.posterior(gi)
print(gi_posterior)
