def nutrient_score(value, range):

    # 0 to 50 -> Very Low zone
    # 50 to 75 -> Medium zone
    # 75 to 100 -> High zone

    if value < range["low"]:
        score = value / range["low"] * 50
    elif value < range["medium"]:
        p = (value - range["low"])/(range["medium"] - range["low"])
        score = 50 + p * 25
    elif value < range["high"]:
        p = (value - range["medium"]) / (range["high"] - range["medium"])
        score = 75 + p * 25
    else:
        score = 100

    return min(100, max(0, score)) # fixed




def theoritical_sfi(N, P, K, OC, pH):
    
    # Ranges are ideals limits for productions
    opt_range = {
            "N": { "low": 200, "medium": 400, "high": 600},
            "P": { "low": 10, "medium": 25, "high":50 },
            "K": { "low": 100, "medium": 250, "high": 400 },
            "OC": { "low": 0.5, "medium": 1.0, "high": 2.0 }
    }

    N_nut_score = nutrient_score(N, opt_range["N"])
    P_nut_score = nutrient_score(P, opt_range["P"])
    K_nut_score = nutrient_score(K, opt_range["K"])
    OC_nut_score = nutrient_score(OC, opt_range["OC"])

    penality_factor = 15
    pH_score = max(0, 100 - abs(pH - 6.5) * penality_factor)

    SFI = (0.30 * N_nut_score + 0.25 * P_nut_score + 0.20 * K_nut_score + 0.15 * OC_nut_score + 0.1 * pH_score)
    
    return round(SFI, 2)



def sfi_for_row(row):
    return theoritical_sfi(row["N"], row["P"], row["K"], row["OC"], row["ph"])



def sfi_dataset(data):
    data["SFI"] = data.apply(sfi_for_row, axis=1)

    # some values
    sfi_mean = round(data["SFI"].mean(), 2)
    sfi_min = round(data["SFI"].min(), 2)
    sfi_max = round(data["SFI"].max(), 2)
    sfi_std = round(data["SFI"].std(), 2)

    sfi_low_count = len(data[data["SFI"] < 40])
    sfi_low_mid_count = len(data[(data["SFI"] >= 40) & (data["SFI"] < 60)])
    sfi_mid_high_count = len(data[(data["SFI"] >= 60) & (data["SFI"] < 80)])
    sfi_high_count = len(data[data["SFI"] >= 80])

    sfi_low_percent = (sfi_low_count / len(data)) * 100  
    sfi_low_mid_percent =(sfi_low_mid_count / len(data)) * 100  
    sfi_mid_high_percent =(sfi_mid_high_count / len(data)) * 100 
    sfi_high_percent = (sfi_high_count / len(data)) * 100 
    
    return data
