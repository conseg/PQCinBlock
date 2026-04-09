from BlockSim.InputsConfig import InputsConfig as p
from BlockSim.Event import Event, Queue
from BlockSim.Scheduler import Scheduler
from BlockSim.Statistics import Statistics
import csv
import os
import sys
import logging
import pandas as pd
from time import time

if p.model == 3:
    from BlockSim.Models.AppendableBlock.BlockCommit import BlockCommit
    from BlockSim.Models.Consensus import Consensus
    from BlockSim.Models.AppendableBlock.Transaction import FullTransaction as FT
    from BlockSim.Models.AppendableBlock.Node import Node
    from BlockSim.Models.Incentives import Incentives
    from BlockSim.Models.AppendableBlock.Statistics import Statistics
    from BlockSim.Models.AppendableBlock.Verification import Verification

elif p.model == 2:
    from BlockSim.Models.Ethereum.BlockCommit import BlockCommit
    from BlockSim.Models.Ethereum.Consensus import Consensus
    from BlockSim.Models.Ethereum.Transaction import LightTransaction as LT, FullTransaction as FT
    from BlockSim.Models.Ethereum.Node import Node
    from BlockSim.Models.Ethereum.Incentives import Incentives

elif p.model == 1:
    from BlockSim.Models.Bitcoin.BlockCommit import BlockCommit
    from BlockSim.Models.Bitcoin.Consensus import Consensus
    from BlockSim.Models.Transaction import LightTransaction as LT, FullTransaction as FT
    from BlockSim.Models.Bitcoin.Node import Node
    from BlockSim.Models.Incentives import Incentives

elif p.model == 0:
    from BlockSim.Models.BlockCommit import BlockCommit
    from BlockSim.Models.Consensus import Consensus
    from BlockSim.Models.Transaction import LightTransaction as LT, FullTransaction as FT
    from BlockSim.Models.Node import Node
    from BlockSim.Models.Incentives import Incentives

########################################################## Start Simulation ##############################################################


def main():
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:         
        df = pd.read_csv(input_file, index_col=False)
        for index, line in df.iterrows():
            p.variant = line["variant"]
            logging.info(f"\tRunning {p.variant}...")
            try:                
                p.mean_verify = float(line["mean_verify"])
                p.std_verify = float(line["std_verify"])
                # p.mean_creation = float(line["mean_creation"])
                # p.std_creation = float(line["std_creation"])
                
                p.mean_artifacts_size = 0
                p.std_artifacts_size = 0
                # Scenario 1: signature size only
                if p.simulation_scenario == 1:
                    p.mean_artifacts_size = float(line["mean_sigSize"])
                    p.std_artifacts_size = float(line["std_sigSize"])
                
                # Scenario 2: signature + public key size
                if p.simulation_scenario == 2:
                    p.mean_artifacts_size = float(line["mean_sigSize"]) + float(line["mean_publicKeySize"])
                    p.std_artifacts_size = float(line["std_sigSize"]) + float(line["std_publicKeySize"])
                
                # Scenario 3: signature * n + 1 * public key size
                if p.simulation_scenario == 3:
                    p.mean_artifacts_size = float(line["mean_sigSize"])
                    p.std_artifacts_size = float(line["std_sigSize"])
                    p.mean_publicKeySize = float(line["mean_publicKeySize"])
                    p.std_publicKeySize = float(line["std_publicKeySize"])

            except Exception as e:
                logging.exception(e)
            try:
                Statistics.index = 0
                for i in range(p.Runs):
                # for i in range(runs):
                    # start_simulation = time()
                    clock = 0  # set clock to 0 at the start of the simulation
                    if p.hasTrans:
                        if p.Ttechnique == "Light":
                            LT.create_transactions()  # generate pending transactions
                        elif p.Ttechnique == "Full":
                            FT.create_transactions()  # generate pending transactions

                    Node.generate_gensis_block()  # generate the gensis block for all miners
                    # initiate initial events >= 1 to start with
                    BlockCommit.generate_initial_events()

                    while not Queue.isEmpty() and clock <= p.simTime:
                        next_event = Queue.get_next_event()
                        clock = next_event.time  # move clock to the time of the event
                        BlockCommit.handle_event(next_event)
                        Queue.remove_event(next_event)

                    # for the AppendableBlock process transactions and
                    # optionally verify the model implementation
                    if p.model == 3:
                        BlockCommit.process_gateway_transaction_pools()

                        if i == 0 and p.VerifyImplemetation:
                            Verification.perform_checks()
                    # end_simulation = time()
                    # print((end_simulation - start_simulation) * 1000)
                    Consensus.fork_resolution()  # apply the longest chain to resolve the forks
                    # distribute the rewards between the particiapting nodes
                    Incentives.distribute_rewards()
                    # calculate the simulation results (e.g., block statstics and miners' rewards)
                    Statistics.calculate()

                    if p.model == 3:
                        Statistics.print_to_excel(i, True)
                        Statistics.reset()
                    else:
                        # os.makedirs("results",exist_ok=True)
                        ########## reset all global variable before the next run #############
                        Statistics.reset()  # reset all variables used to calculate the results
                        Node.resetState()  # reset all the states (blockchains) for all nodes in the network
                        # fname = "results/{0}(Allverify)1day_{1}M_{2}K.xlsx".format(p.variant, p.Bsize/1000000, p.Tn/1000)
                        # print all the simulation results in an excel file
                        # Statistics.print_to_excel(fname)
                        # fname = "results/{0}(Allverify)1day_{1}M_{2}K.xlsx".format(p.variant, p.Bsize/1000000, p.Tn/1000)
                        # print all the simulation results in an excel file
                        # Statistics.print_to_excel(fname)
                        try:
                            Statistics.print_to_csv(output_file)
                        except Exception as e:
                            print("Error ("+str(e)+") in print csv")
                        Statistics.reset2()  # reset profit results
            except Exception as e:
                print("Error ("+str(e)+") in main loop")
    except Exception as e:
        print(e)


######################################################## Run Main method #####################################################################
if __name__ == '__main__':
    main()
