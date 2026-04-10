# ===============================
# IMPORTS
# ===============================
import pandas as pd
import glob
import numpy as np

# =========================================
# SETTINGS (CHANGE THIS IF NEEDED)
# =========================================
SAMPLE_SIZE = 30000   # rows per file (IMPORTANT)

# =========================================
# MEMORY OPTIMIZATION FUNCTION
# =========================================
def reduce_memory(df):
    for col in df.columns:
        if df[col].dtype == 'float64':
            df[col] = df[col].astype('float32')
        elif df[col].dtype == 'int64':
            df[col] = df[col].astype('int32')
    return df

# =========================================
# LOAD + SAMPLE + LABEL
# =========================================
def load_dataset(path_pattern, attack_name):
    files = glob.glob(path_pattern)
    
    print(f"\nProcessing: {attack_name}")
    
    if len(files) == 0:
        print("❌ No files found")
        return pd.DataFrame()
    
    df_list = []
    
    for file in files:
        try:
            temp = pd.read_csv(file)
            
            # 🔥 SAMPLE (MOST IMPORTANT)
            if len(temp) > SAMPLE_SIZE:
                temp = temp.sample(n=SAMPLE_SIZE, random_state=42)
            
            temp["Attack_Type"] = attack_name
            
            temp = reduce_memory(temp)  # optimize memory
            
            df_list.append(temp)
            
            print(f"Loaded: {file} | Shape: {temp.shape}")
        
        except Exception as e:
            print(f"Error: {file} → {e}")
    
    return pd.concat(df_list, ignore_index=True)


# ===============================
# LOAD ALL DATASETS
# ===============================

datasets = []

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-ACK_Fragmentation/*.csv", "DDoS_ACK_Fragmentation"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-ICMP_Flood/*.csv", "DDoS_ICMP_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-ICMP_Fragmentation/*.csv", "DDoS_ICMP_Fragmentation"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-PSHACK_FLOOD/*.csv", "DDoS_PSHACK_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-RSTFINFLOOD/*.csv", "DDoS_RSTFIN_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-SYN_Flood/*.csv", "DDoS_SYN_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-SynonymousIP_Flood/*.csv", "DDoS_SynonymousIP_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-TCP_Flood/*.csv", "DDoS_TCP_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-UDP_Flood/*.csv", "DDoS_UDP_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-UDP_Fragmentation/*.csv", "DDoS_UDP_Fragmentation"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DoS-HTTP_Flood/*.csv", "DoS_HTTP_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DoS-SYN_Flood/*.csv", "DoS_SYN_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DoS-TCP_Flood/*.csv", "DoS_TCP_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/DoS-UDP_Flood/*.csv", "DoS_UDP_Flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/Mirai-greeth_flood/*.csv", "Mirai_greeth_flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/Mirai-greip_flood/*.csv", "Mirai_greip_flood"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/Mirai-udpplain/*.csv", "Mirai_udpplain"))

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/MITM-ArpSpoofing/*.csv", "MITM_ArpSpoofing"))

# ===============================
# SINGLE FILE DATASETS
# ===============================

def load_single(file_path, attack_name):
    try:
        df = pd.read_csv(file_path)
        df["Attack_Type"] = attack_name
        print(f"✅ {attack_name}:", df.shape)
        return df
    except:
        print(f"❌ Error loading {attack_name}")
        return pd.DataFrame()

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/Backdoor_Malware/Backdoor_Malware.pcap.csv", "Backdoor"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/BrowserHijacking/BrowserHijacking.pcap.csv", "BrowserHijacking"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/CommandInjection/CommandInjection.pcap.csv", "CommandInjection"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-HTTP_Flood/DDoS-HTTP_Flood-.pcap.csv", "DDoS_HTTP_Flood"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/DDoS-SlowLoris/DDoS-SlowLoris.pcap.csv", "DDoS_SlowLoris"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/DictionaryBruteForce/DictionaryBruteForce.pcap.csv", "BruteForce"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/DNS_Spoofing/DNS_Spoofing.pcap.csv", "DNS_Spoofing"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/Recon-HostDiscovery/Recon-HostDiscovery.pcap.csv", "Recon_HostDiscovery"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/Recon-OSScan/Recon-OSScan.pcap.csv", "Recon_OSScan"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/Recon-PingSweep/Recon-PingSweep.pcap.csv", "Recon_PingSweep"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/Recon-PortScan/Recon-PortScan.pcap.csv", "Recon_PortScan"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/SqlInjection/SqlInjection.pcap.csv", "SQL_Injection"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/Uploading_Attack/Uploading_Attack.pcap.csv", "Uploading_Attack"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/VulnerabilityScan/VulnerabilityScan.pcap.csv", "VulnerabilityScan"))

datasets.append(load_single("/Users/taushi/Downloads/python/DATA_science/CSV/XSS/XSS.pcap.csv", "XSS"))

# ===============================
# BENIGN DATA
# ===============================

benign_files = glob.glob("/Users/taushi/Downloads/python/DATA_science/CSV/Benign_Final/*.csv")

datasets.append(load_dataset("/Users/taushi/Downloads/python/DATA_science/CSV/Benign_Final/*.csv", "Benign"))

# ===============================
# FINAL MERGE
# ===============================

# Remove empty datasets
datasets = [df for df in datasets if not df.empty]

final_df = pd.concat(datasets, ignore_index=True)

print("\n🔥 FINAL DATASET SHAPE:", final_df.shape)

# =========================================
# CLEANING
# =========================================
final_df.replace([np.inf, -np.inf], np.nan, inplace=True)
final_df.dropna(inplace=True)
final_df.drop_duplicates(inplace=True)

print("🔥 Final Shape AFTER CLEANING:", final_df.shape)
# # BALANCE DATASET (VERY IMPORTANT)
# # =========================================
# min_count = final_df['Attack_Type'].value_counts().min()

# balanced_df = final_df.groupby('Attack_Type').sample(n=min_count)

# print("🔥 Balanced Dataset Shape:", balanced_df.shape)

# # =========================================
# # BALANCE DATASET (VERY IMPORTANT)
# # =========================================
# min_count = final_df['Attack_Type'].value_counts().min()

# balanced_df = final_df.groupby('Attack_Type').sample(n=min_count)

# print("🔥 Balanced Dataset Shape:", balanced_df.shape)






# ===============================
# SAVE FINAL DATASET
# ===============================
final_df.to_csv("FINAL_IOT_DATASET.csv", index=False)

print("✅ Final dataset saved as FINAL_IOT_DATASET.csv")