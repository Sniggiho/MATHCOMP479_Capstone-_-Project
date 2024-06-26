import networkx
import random

def generateTransFreqMap(file):
    """Given a csv edgelist, creates a map with edges as the keys and frequencies as the notes"""
    freqs = {}

    f = open(file)
    
    for line in f.readlines():
        line = line.strip()
        if line in freqs.keys():
            freqs[line]+=1
        else:
            freqs[line] = 1

    return freqs

def getNoteDuration(note):
    """Given a note string in the form N_#, returns an integer value representing the number of 32nd notes in that note"""
    # 32 -> 1
    # 16 -> 2
    # 8 -> 4
    # 4 -> 8
    # 2 -> 16
    # 1 -> 32
    num = note.split("_")[1]
    dur = 0
    if "d" in num:
        num = num[:-1]
        dur += 32/(int(num)*2)
    dur += 32/(int(num))

    return dur


def measuredRandomWalk(transFreqs, staringNote = "LA_4",  measureLen = 32, numMeasures = 16, includeStartNote = False):
    """Given a map with keys in format note1,note2 and values containing the number of transitions between those notes 
    does a ranodm walk on those notes to create a tune measure by measure."""
    
    # TODO: some logic to allow a random starting note?

    currNote = staringNote    
    m = 0 # the number of measures generated so far
    mSum = 0 # the total duration of notes in the current measure 
    tune = []
    measure = []

    if includeStartNote:
        measure.append(currNote)
        mSum += getNoteDuration(currNote)

    while m < numMeasures:
                
        if mSum == measureLen:
            mSum = 0
            m += 1
            tune.append(measure)
            measure = []

        neighbors = []
        weights = []
        for key in transFreqs.keys():
            if currNote in key.split(",")[0]:
                n = key.split(",")[1]
                if getNoteDuration(n) <= measureLen - mSum: # if the note will fit in what we have left of the measure
                    neighbors.append(key.split(",")[1])
                    weights.append(transFreqs[key])
        if len(neighbors) == 0:
            raise Exception("No legal neighbor")

        currNote  = random.choices(neighbors,weights=weights,k=1)[0]
        measure.append(currNote)

        mSum += getNoteDuration(currNote)

    return tune



#TODO: 
# - beat by beat to avoid weird ass ties when possible
# - recursive to defeat "No legal note" exception
# - phrase by phrase to create believable bagpipe structure?
# - ways to bake in more structure via the network itself?
if __name__ == "__main__":
    tune = measuredRandomWalk(generateTransFreqMap("Note Networks/All Jigs.csv"), staringNote="E_8", measureLen=24, numMeasures=4, includeStartNote = False)
    print(tune)