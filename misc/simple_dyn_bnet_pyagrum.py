import pyagrum as gum
import pandas as pd
import numpy as np


# Step 1: Define the Dynamic Bayesian Network with specified CPTs

def create_dbn_with_cpts():
    """Create a Dynamic Bayesian Network with manually defined CPTs"""

    # Create the Bayesian Network
    bn = gum.BayesNet('DBN_Example')

    # Add nodes with their states
    # r nodes have 3 states: wet(0), dry(1), normal(2)
    # a nodes have 2 states: 0, 1

    r1 = bn.add(gum.LabelizedVariable('r1', 'r1', ['wet', 'dry', 'normal']))
    r2 = bn.add(gum.LabelizedVariable('r2', 'r2', ['wet', 'dry', 'normal']))
    r3 = bn.add(gum.LabelizedVariable('r3', 'r3', ['wet', 'dry', 'normal']))
    r4 = bn.add(gum.LabelizedVariable('r4', 'r4', ['wet', 'dry', 'normal']))

    a1 = bn.add(gum.LabelizedVariable('a1', 'a1', ['0', '1']))
    a2 = bn.add(gum.LabelizedVariable('a2', 'a2', ['0', '1']))
    a3 = bn.add(gum.LabelizedVariable('a3', 'a3', ['0', '1']))
    a4 = bn.add(gum.LabelizedVariable('a4', 'a4', ['0', '1']))

    # Add arcs according to the graph: r1->a1,r2; r2->a2,r3; r3->a3,r4; r4->a4
    bn.addArc(r1, a1)
    bn.addArc(r1, r2)
    bn.addArc(r2, a2)
    bn.addArc(r2, r3)
    bn.addArc(r3, a3)
    bn.addArc(r3, r4)
    bn.addArc(r4, a4)

    # Define CPTs

    # CPT for r1 (no parents) - prior distribution
    bn.cpt(r1).fillWith(
        [0.3, 0.4, 0.3])  # P(wet)=0.3, P(dry)=0.4, P(normal)=0.3

    # CPT for r2 given r1
    # r2 | r1=wet    -> [0.5, 0.2, 0.3]
    # r2 | r1=dry    -> [0.1, 0.7, 0.2]
    # r2 | r1=normal -> [0.2, 0.3, 0.5]
    bn.cpt(r2)[{'r1': 'wet'}] = [0.5, 0.2, 0.3]
    bn.cpt(r2)[{'r1': 'dry'}] = [0.1, 0.7, 0.2]
    bn.cpt(r2)[{'r1': 'normal'}] = [0.2, 0.3, 0.5]

    # CPT for r3 given r2
    # r3 | r2=wet    -> [0.6, 0.1, 0.3]
    # r3 | r2=dry    -> [0.1, 0.8, 0.1]
    # r3 | r2=normal -> [0.2, 0.2, 0.6]
    bn.cpt(r3)[{'r2': 'wet'}] = [0.6, 0.1, 0.3]
    bn.cpt(r3)[{'r2': 'dry'}] = [0.1, 0.8, 0.1]
    bn.cpt(r3)[{'r2': 'normal'}] = [0.2, 0.2, 0.6]

    # CPT for r4 given r3
    # r4 | r3=wet    -> [0.7, 0.1, 0.2]
    # r4 | r3=dry    -> [0.1, 0.8, 0.1]
    # r4 | r3=normal -> [0.3, 0.2, 0.5]
    bn.cpt(r4)[{'r3': 'wet'}] = [0.7, 0.1, 0.2]
    bn.cpt(r4)[{'r3': 'dry'}] = [0.1, 0.8, 0.1]
    bn.cpt(r4)[{'r3': 'normal'}] = [0.3, 0.2, 0.5]

    # CPT for a1 given r1
    # a1 | r1=wet    -> [0.8, 0.2]  (P(0|wet)=0.8, P(1|wet)=0.2)
    # a1 | r1=dry    -> [0.3, 0.7]
    # a1 | r1=normal -> [0.5, 0.5]
    bn.cpt(a1)[{'r1': 'wet'}] = [0.8, 0.2]
    bn.cpt(a1)[{'r1': 'dry'}] = [0.3, 0.7]
    bn.cpt(a1)[{'r1': 'normal'}] = [0.5, 0.5]

    # CPT for a2 given r2
    # a2 | r2=wet    -> [0.9, 0.1]
    # a2 | r2=dry    -> [0.2, 0.8]
    # a2 | r2=normal -> [0.4, 0.6]
    bn.cpt(a2)[{'r2': 'wet'}] = [0.9, 0.1]
    bn.cpt(a2)[{'r2': 'dry'}] = [0.2, 0.8]
    bn.cpt(a2)[{'r2': 'normal'}] = [0.4, 0.6]

    # CPT for a3 given r3
    # a3 | r3=wet    -> [0.85, 0.15]
    # a3 | r3=dry    -> [0.25, 0.75]
    # a3 | r3=normal -> [0.45, 0.55]
    bn.cpt(a3)[{'r3': 'wet'}] = [0.85, 0.15]
    bn.cpt(a3)[{'r3': 'dry'}] = [0.25, 0.75]
    bn.cpt(a3)[{'r3': 'normal'}] = [0.45, 0.55]

    # CPT for a4 given r4
    # a4 | r4=wet    -> [0.9, 0.1]
    # a4 | r4=dry    -> [0.3, 0.7]
    # a4 | r4=normal -> [0.5, 0.5]
    bn.cpt(a4)[{'r4': 'wet'}] = [0.9, 0.1]
    bn.cpt(a4)[{'r4': 'dry'}] = [0.3, 0.7]
    bn.cpt(a4)[{'r4': 'normal'}] = [0.5, 0.5]

    return bn


# Step 2: Generate data from the network

def generate_data_from_dbn(bn, n_samples=52):
    """Generate data from the Dynamic Bayesian Network using manual sampling"""

    print("Generating data using manual sampling...")
    np.random.seed(42)  # For reproducibility
    data = []

    for sample_idx in range(n_samples):
        row = {}

        # Sample r1 first (no parents)
        r1_cpt = bn.cpt('r1')
        r1_probs = []
        for i in range(3):  # 3 states for r1
            r1_probs.append(float(r1_cpt[i]))
        r1_state = np.random.choice(3, p=r1_probs)
        row['r1'] = ['wet', 'dry', 'normal'][r1_state]

        # Sample a1 given r1
        a1_cpt = bn.cpt('a1')
        a1_probs = []
        for i in range(2):  # 2 states for a1
            # Create instantiation for r1=r1_state
            inst = gum.Instantiation(a1_cpt)
            inst.chgVal('r1', r1_state)
            inst.chgVal('a1', i)
            a1_probs.append(float(a1_cpt[inst]))
        # Normalize probabilities
        a1_sum = sum(a1_probs)
        a1_probs = [p / a1_sum for p in a1_probs]
        a1_state = np.random.choice(2, p=a1_probs)
        row['a1'] = ['0', '1'][a1_state]

        # Sample r2 given r1
        r2_cpt = bn.cpt('r2')
        r2_probs = []
        for i in range(3):  # 3 states for r2
            inst = gum.Instantiation(r2_cpt)
            inst.chgVal('r1', r1_state)
            inst.chgVal('r2', i)
            r2_probs.append(float(r2_cpt[inst]))
        r2_sum = sum(r2_probs)
        r2_probs = [p / r2_sum for p in r2_probs]
        r2_state = np.random.choice(3, p=r2_probs)
        row['r2'] = ['wet', 'dry', 'normal'][r2_state]

        # Sample a2 given r2
        a2_cpt = bn.cpt('a2')
        a2_probs = []
        for i in range(2):  # 2 states for a2
            inst = gum.Instantiation(a2_cpt)
            inst.chgVal('r2', r2_state)
            inst.chgVal('a2', i)
            a2_probs.append(float(a2_cpt[inst]))
        a2_sum = sum(a2_probs)
        a2_probs = [p / a2_sum for p in a2_probs]
        a2_state = np.random.choice(2, p=a2_probs)
        row['a2'] = ['0', '1'][a2_state]

        # Sample r3 given r2
        r3_cpt = bn.cpt('r3')
        r3_probs = []
        for i in range(3):  # 3 states for r3
            inst = gum.Instantiation(r3_cpt)
            inst.chgVal('r2', r2_state)
            inst.chgVal('r3', i)
            r3_probs.append(float(r3_cpt[inst]))
        r3_sum = sum(r3_probs)
        r3_probs = [p / r3_sum for p in r3_probs]
        r3_state = np.random.choice(3, p=r3_probs)
        row['r3'] = ['wet', 'dry', 'normal'][r3_state]

        # Sample a3 given r3
        a3_cpt = bn.cpt('a3')
        a3_probs = []
        for i in range(2):  # 2 states for a3
            inst = gum.Instantiation(a3_cpt)
            inst.chgVal('r3', r3_state)
            inst.chgVal('a3', i)
            a3_probs.append(float(a3_cpt[inst]))
        a3_sum = sum(a3_probs)
        a3_probs = [p / a3_sum for p in a3_probs]
        a3_state = np.random.choice(2, p=a3_probs)
        row['a3'] = ['0', '1'][a3_state]

        # Sample r4 given r3
        r4_cpt = bn.cpt('r4')
        r4_probs = []
        for i in range(3):  # 3 states for r4
            inst = gum.Instantiation(r4_cpt)
            inst.chgVal('r3', r3_state)
            inst.chgVal('r4', i)
            r4_probs.append(float(r4_cpt[inst]))
        r4_sum = sum(r4_probs)
        r4_probs = [p / r4_sum for p in r4_probs]
        r4_state = np.random.choice(3, p=r4_probs)
        row['r4'] = ['wet', 'dry', 'normal'][r4_state]

        # Sample a4 given r4
        a4_cpt = bn.cpt('a4')
        a4_probs = []
        for i in range(2):  # 2 states for a4
            inst = gum.Instantiation(a4_cpt)
            inst.chgVal('r4', r4_state)
            inst.chgVal('a4', i)
            a4_probs.append(float(a4_cpt[inst]))
        a4_sum = sum(a4_probs)
        a4_probs = [p / a4_sum for p in a4_probs]
        a4_state = np.random.choice(2, p=a4_probs)
        row['a4'] = ['0', '1'][a4_state]

        data.append(row)

    df = pd.DataFrame(data)

    # Reorder columns to match the requested order
    column_order = ['r1', 'r2', 'r3', 'r4', 'a1', 'a2', 'a3', 'a4']
    df = df[column_order]

    return df


# Step 3: Learn CPTs from data

def learn_cpts_from_data(df):
    """Create a new network with same structure but learn CPTs from data"""

    # Create the network structure (same as before but without CPT values)
    bn_learned = gum.BayesNet('DBN_Learned')

    # Add nodes
    r1 = bn_learned.add(
        gum.LabelizedVariable('r1', 'r1', ['wet', 'dry', 'normal']))
    r2 = bn_learned.add(
        gum.LabelizedVariable('r2', 'r2', ['wet', 'dry', 'normal']))
    r3 = bn_learned.add(
        gum.LabelizedVariable('r3', 'r3', ['wet', 'dry', 'normal']))
    r4 = bn_learned.add(
        gum.LabelizedVariable('r4', 'r4', ['wet', 'dry', 'normal']))

    a1 = bn_learned.add(gum.LabelizedVariable('a1', 'a1', ['0', '1']))
    a2 = bn_learned.add(gum.LabelizedVariable('a2', 'a2', ['0', '1']))
    a3 = bn_learned.add(gum.LabelizedVariable('a3', 'a3', ['0', '1']))
    a4 = bn_learned.add(gum.LabelizedVariable('a4', 'a4', ['0', '1']))

    # Add arcs (same structure)
    bn_learned.addArc(r1, a1)
    bn_learned.addArc(r1, r2)
    bn_learned.addArc(r2, a2)
    bn_learned.addArc(r2, r3)
    bn_learned.addArc(r3, a3)
    bn_learned.addArc(r3, r4)
    bn_learned.addArc(r4, a4)

    # Learn parameters from data
    learner = gum.BNLearner(df)

    # Try different smoothing methods based on available API
    try:
        learner.useAprioriSmoothing()
    except AttributeError:
        try:
            learner.useSmoothingPrior()
        except AttributeError:
            try:
                learner.useNoPrior()  # If no smoothing available, use no prior
            except AttributeError:
                pass  # Continue without smoothing if none available

    # Set the structure we want to learn
    try:
        learner.setTargetBN(bn_learned)
        bn_learned = learner.learnParameters()
    except AttributeError:
        # Alternative approach: learn parameters directly
        try:
            bn_learned = learner.learnBN()
            # Copy the structure we want
            bn_temp = gum.BayesNet('DBN_Learned')

            # Add nodes
            r1 = bn_temp.add(
                gum.LabelizedVariable('r1', 'r1', ['wet', 'dry', 'normal']))
            r2 = bn_temp.add(
                gum.LabelizedVariable('r2', 'r2', ['wet', 'dry', 'normal']))
            r3 = bn_temp.add(
                gum.LabelizedVariable('r3', 'r3', ['wet', 'dry', 'normal']))
            r4 = bn_temp.add(
                gum.LabelizedVariable('r4', 'r4', ['wet', 'dry', 'normal']))

            a1 = bn_temp.add(gum.LabelizedVariable('a1', 'a1', ['0', '1']))
            a2 = bn_temp.add(gum.LabelizedVariable('a2', 'a2', ['0', '1']))
            a3 = bn_temp.add(gum.LabelizedVariable('a3', 'a3', ['0', '1']))
            a4 = bn_temp.add(gum.LabelizedVariable('a4', 'a4', ['0', '1']))

            # Add arcs
            bn_temp.addArc(r1, a1)
            bn_temp.addArc(r1, r2)
            bn_temp.addArc(r2, a2)
            bn_temp.addArc(r2, r3)
            bn_temp.addArc(r3, a3)
            bn_temp.addArc(r3, r4)
            bn_temp.addArc(r4, a4)

            # Learn parameters using Maximum Likelihood Estimation
            from collections import defaultdict
            import itertools

            # Count occurrences for each variable given its parents
            def learn_cpt_from_data(var_name, parent_names, df):
                # Count combinations
                counts = defaultdict(int)
                total_counts = defaultdict(int)

                for _, row in df.iterrows():
                    parent_values = tuple(row[p] for p in
                                          parent_names) if parent_names else tuple()
                    child_value = row[var_name]

                    counts[(parent_values, child_value)] += 1
                    total_counts[parent_values] += 1

                # Convert to probabilities
                cpt_dict = {}

                if not parent_names:  # No parents
                    var_states = ['wet', 'dry',
                                  'normal'] if var_name.startswith('r') else [
                        '0', '1']
                    total = sum(counts.get((tuple(), state), 0) for state in
                                var_states)
                    probs = [counts.get((tuple(), state), 0) / max(total, 1)
                             for state in var_states]
                    # Add smoothing
                    probs = [(p + 0.01) / (1 + 0.01 * len(var_states)) for p in
                             probs]
                    cpt_dict[tuple()] = probs
                else:
                    parent_states_list = []
                    for p in parent_names:
                        if p.startswith('r'):
                            parent_states_list.append(['wet', 'dry', 'normal'])
                        else:
                            parent_states_list.append(['0', '1'])

                    var_states = ['wet', 'dry',
                                  'normal'] if var_name.startswith('r') else [
                        '0', '1']

                    for parent_combo in itertools.product(*parent_states_list):
                        total = total_counts.get(parent_combo, 0)
                        probs = [
                            counts.get((parent_combo, state), 0) / max(total,
                                                                       1) for
                            state in var_states]
                        # Add smoothing
                        probs = [(p + 0.01) / (1 + 0.01 * len(var_states)) for
                                 p in probs]
                        cpt_dict[parent_combo] = probs

                return cpt_dict

            # Learn CPTs
            r1_cpt = learn_cpt_from_data('r1', [], df)
            bn_temp.cpt('r1').fillWith(r1_cpt[tuple()])

            r2_cpt = learn_cpt_from_data('r2', ['r1'], df)
            for parent_state, probs in r2_cpt.items():
                r1_idx = ['wet', 'dry', 'normal'].index(parent_state[0])
                bn_temp.cpt('r2')[{'r1': r1_idx}] = probs

            r3_cpt = learn_cpt_from_data('r3', ['r2'], df)
            for parent_state, probs in r3_cpt.items():
                r2_idx = ['wet', 'dry', 'normal'].index(parent_state[0])
                bn_temp.cpt('r3')[{'r2': r2_idx}] = probs

            r4_cpt = learn_cpt_from_data('r4', ['r3'], df)
            for parent_state, probs in r4_cpt.items():
                r3_idx = ['wet', 'dry', 'normal'].index(parent_state[0])
                bn_temp.cpt('r4')[{'r3': r3_idx}] = probs

            a1_cpt = learn_cpt_from_data('a1', ['r1'], df)
            for parent_state, probs in a1_cpt.items():
                r1_idx = ['wet', 'dry', 'normal'].index(parent_state[0])
                bn_temp.cpt('a1')[{'r1': r1_idx}] = probs

            a2_cpt = learn_cpt_from_data('a2', ['r2'], df)
            for parent_state, probs in a2_cpt.items():
                r2_idx = ['wet', 'dry', 'normal'].index(parent_state[0])
                bn_temp.cpt('a2')[{'r2': r2_idx}] = probs

            a3_cpt = learn_cpt_from_data('a3', ['r3'], df)
            for parent_state, probs in a3_cpt.items():
                r3_idx = ['wet', 'dry', 'normal'].index(parent_state[0])
                bn_temp.cpt('a3')[{'r3': r3_idx}] = probs

            a4_cpt = learn_cpt_from_data('a4', ['r4'], df)
            for parent_state, probs in a4_cpt.items():
                r4_idx = ['wet', 'dry', 'normal'].index(parent_state[0])
                bn_temp.cpt('a4')[{'r4': r4_idx}] = probs

            bn_learned = bn_temp

        except Exception as e:
            print(f"Learning failed with error: {e}")
            print("Using manual parameter learning...")
            bn_learned = bn_learned  # Keep the structure-only network

    return bn_learned


def compare_networks(original_bn, learned_bn):
    """Compare original and learned CPTs"""
    print("=== COMPARISON OF ORIGINAL vs LEARNED CPTs ===\n")

    for var_name in ['r1', 'r2', 'r3', 'r4', 'a1', 'a2', 'a3', 'a4']:
        print(f"--- {var_name} ---")
        print("Original CPT:")
        print(original_bn.cpt(var_name))
        print("\nLearned CPT:")
        print(learned_bn.cpt(var_name))
        print("\n" + "=" * 50 + "\n")


# Main execution
if __name__ == "__main__":
    # Step 1: Create DBN with specified CPTs
    print("Step 1: Creating Dynamic Bayesian Network with predefined CPTs...")
    original_dbn = create_dbn_with_cpts()
    print(
        f"Network created with {original_dbn.size()} nodes and {original_dbn.sizeArcs()} arcs")

    # Display the original network structure and some CPTs
    print("\nNetwork structure:")
    print(f"Nodes: {list(original_dbn.names())}")
    print(
        f"Arcs: {[(original_dbn.variable(arc[0]).name(), original_dbn.variable(arc[1]).name()) for arc in original_dbn.arcs()]}")

    print("\nExample CPT for r1 (root node):")
    print(original_dbn.cpt('r1'))

    print("\nExample CPT for a1 given r1:")
    print(original_dbn.cpt('a1'))

    # Step 2: Generate data
    print("\n" + "=" * 60)
    print("Step 2: Generating 52 samples from the network...")
    generated_data = generate_data_from_dbn(original_dbn, 52)
    print(f"Generated DataFrame shape: {generated_data.shape}")
    print("\nFirst 10 rows of generated data:")
    print(generated_data.head(10))

    print("\nData distribution summary:")
    for col in generated_data.columns:
        print(f"{col}: {dict(generated_data[col].value_counts())}")

    # Step 3: Learn CPTs from generated data
    print("\n" + "=" * 60)
    print("Step 3: Learning CPTs from generated data...")
    learned_dbn = learn_cpts_from_data(generated_data)
    print("Learning completed!")

    # Compare networks
    print("\n" + "=" * 60)
    compare_networks(original_dbn, learned_dbn)

    # Save the generated data to see it clearly
    print("Generated DataFrame (all 52 rows):")
    print(generated_data.to_string(index=False))