# Simulate brand perception survey data
import pandas as pd
import numpy as np

def generateHalo(mean = 5, stdev = 5, size = 1000): # Generate halo effect for each respondent
    rng = np.random.default_rng(2021) # Set seed only for this function and not globally
    halo = rng.normal(loc = mean, scale = stdev, size = size)
    return halo

def generateScores(halo, scoreRange = (0, 10)): # Generate scores for 1 column
    mean = np.random.uniform(scoreRange[0], scoreRange[1]) # Set mean
    stdev = np.random.uniform(scoreRange[0], scoreRange[1]) # Set standard deviation
    scores = np.random.normal(loc = mean, scale = stdev, size = len(halo))
    scores = np.floor(scores + halo) # Add halo effect and use floor to get integers
    scores = np.clip(scores, scoreRange[0], scoreRange[1]) # Limit values to be within range
    return scores

def generateBrandScores(halo, brand = 'a'): # Generate scores for all columns
    columns = ['perform', 'leader', 'latest', 'fun', 'serious', 'bargain', 'value', 'trendy', 'rebuy', 'brand']
    df = pd.DataFrame()
    for i in columns:
        columnScores = generateScores(halo) if i != 'brand' else np.repeat(brand, len(halo))
        df = pd.concat([df, pd.DataFrame(columnScores)], axis = 1)
    df = df.reset_index(drop = True)
    df.columns = columns
    return df

def generateBrandSurvey(halo, brands = ['a','b','c','d','e','f','g','h','i','j']): # Generate scores for all brands
    df = pd.DataFrame()
    for i in brands:
        dfBrand = generateBrandScores(halo, brand = i)
        df = pd.concat([df, dfBrand], axis = 0)
    df = df.reset_index(drop = True)
    return df

def main():
    halo = generateHalo()
    df = generateBrandSurvey(halo)
    return df

if __name__ == '__main__':
    df= main()
df