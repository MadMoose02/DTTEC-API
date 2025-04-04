from json import loads

candidates = []
with open("DTTEC_FULL.json", "r", encoding="utf-8") as f:
    for entry in loads(f.read()):
        headword = entry['headword'].split(" ")[0]
        if len(headword) > 20: continue
        if headword == '' or headword is None or len(headword) < 1: continue
        if headword in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']: continue
        if headword in candidates: continue
        
        # Check if word has alternating vowel and consonant spellings
        start = headword[0]
        if start in 'aeiou':
            for i in range(1, len(headword)):
                if i % 2 == 0 and headword[i] not in 'aeiou': break
                if i % 2 == 1 and headword[i] in 'aeiou': break
                
            candidates.append(headword)

print(candidates)