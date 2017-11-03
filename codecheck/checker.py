import sys
import csv

# Functions to check for video files
error_log = []
acceptable_utterance_types = ['s', 'n', 'd', 'r', 'q', 'i', 'o', 'u']
comment = "%com:"


def check_ordinal_video(ordinal, line_number, word, total_lines, ordinal_list):
    digit_list = ['0']
    for y in ordinal:
        if y.isdigit():
            digit_list.append(y)
    string_digits = ''.join(digit_list)
    int_digits = int(string_digits)
    
    try:
        #Check for repeat values
        assert(not (ordinal in ordinal_list))
        #Check for non-digit characters
        assert(x.isdigit() for x in ordinal)
        #Check that ordinal value is from 1 to total_lines-1, inclusive
        assert(int_digits >= 0 and int_digits <= total_lines - 1)

    except AssertionError:
        return False

    return True
    

def check_onset_video(onset, line_number, word):
    try:
        assert(x.isdigit() for x in onset)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.onset"])
        return False

    return True


def check_offset_video(offset, line_number, word):
    try:
        assert(x.isdigit() for x in offset)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.offset"])


def check_object_video(obj, line_number):
    try:
    	if not obj.startswith(comment):
	        for char in obj:
	            assert (char.isalpha() or char == "+" or char == "'")
    except AssertionError:
        error_log.append([obj, line_number, "labeled_object.object"])
        return False

    return True


def check_utterance_type_video(utterance_type, line_number, word):
    try:
    	if word.startswith(comment):
    		assert (utterance_type == "NA")
    	else:
        	assert (utterance_type in acceptable_utterance_types)
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.utterance_type"])
        return False
        
    return True


def check_object_present_video(obj_pres, line_number, word):
    try:
    	if word.startswith(comment):
    		assert (obj_pres == "NA")
    	else:
        	assert(obj_pres == "y" or obj_pres == "n" or obj_pres == "o" or obj_pres == "u")
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.object_present"])
        return False
        
    return True

def isValid(speaker):
    if len(speaker) != 3: return False
    if speaker[0].isalpha() and speaker[0].isupper():
        if speaker[1].isalpha() and speaker[1].isupper():
            if speaker[2].isalpha() and speaker[2].isupper():
                return True
            elif speaker[2].isdigit():
                return True
    return False

def check_speaker_video(speaker, line_number, word):
	try:
            if word.startswith(comment):
		assert (speaker == "NA")
	    else:
		assert(isValid(speaker))
	except AssertionError:
		error_log.append([word, line_number, "labeled_object.speaker"])
        return False
        
    return True


def check_basic_level_video(basic_level, line_number, word):
    try:
    	if word.startswith(comment):
    	    assert (basic_level == "NA")
    	else:
	    for char in basic_level:
	        assert (char.isalpha() or char == "+" or char == "'" or char == " ")
    except AssertionError:
        error_log.append([word, line_number, "labeled_object.basic_level"])
        return False
        
    return True


#Functions to check for audio files

acceptable_tier = ['*CHF', '*CHN', '*CXF', '*CXN', '*FAF', '*FAN', '*NOF',
                   '*MAF', '*MAN', '*NON', '*OLF', '*OLN', '*SIL', '*TVF', '*TVN']

def check_tier_audio(tier, line_number, word):
    try:
        assert(tier in acceptable_tier)
    except AssertionError:
        error_log.append([word, line_number, "tier"])
        return False
        
    return True


def check_word_audio(word, line_number):
    try:
        for char in word:
            assert (char.isalpha() or char == "+" or char == "'")
    except AssertionError:
        error_log.append([word, line_number, "word"])
        return False
        
    return True


def check_utterance_type_audio(utterance_type, line_number, word):
    try:
        assert (utterance_type in acceptable_utterance_types)
    except AssertionError:
        error_log.append([word, line_number, "utterance_type"])
        return False
        
    return True


def check_object_present_audio(obj_pres, line_number, word):
    try:
        assert(obj_pres == "y" or obj_pres == "n" or obj_pres == "u" or obj_pres == "o")
    except AssertionError:
        error_log.append([word, line_number, "object_present"])
        return False
        
    return True


def check_speaker_audio(speaker, line_number,word):
    try:
        if word.startswith(comment):
	    assert (speaker == "NA")
	else:
	    assert(isValid(speaker))
    except AssertionError:
    	error_log.append([word, line_number, "labeled_object.speaker"])
        return False
        
    return True


def check_timestamp_audio(timestamp, line_number, word):
    underscore_index = timestamp.find("_")

    if underscore_index != -1:
        try:
            for x in range(len(timestamp)):
                if x != underscore_index:
                    assert(timestamp[x].isdigit())
        except AssertionError:
            error_log.append([word, line_number, "timestamp"])
    else:
        try:
            assert(underscore_index != -1)
        except AssertionError:
            error_log.append([word, line_number, "timestamp"])
               
    

def check_basic_level_audio(basic_level, line_number, word):
    try:
        for char in basic_level:
            assert (char.isalpha() or char == "+" or char == "'" or char == " ")
    except AssertionError:
        error_log.append([word, line_number, "basic_level"])


def give_error_report_audio(info):
    global error_log
    error_log = []

    colName = info[0]
    for i in range(len(colName)):
        if colName[i] == "tier":
            tierI = i
        elif colName[i] == "word":
            wordI = i
        elif colName[i] == "utterance_type":
            utterI = i
        elif colName[i] == "object_present":
            obj_preI = i
        elif colName[i] == "speaker":
            speakerI = i
        elif colName[i] == "timestamp":
            timestampI = i
        elif colName[i] == "basic_level":
            basicI = i

    line_number = 1
    for row in info: 
        if not line_number == 1:
            check_tier_audio(row[tierI], str(line_number), row[wordI])
            check_word_audio(row[wordI], str(line_number))
            check_utterance_type_audio(row[utterI], str(line_number), row[wordI])
            check_object_present_audio(row[obj_preI], str(line_number), row[wordI])
            check_speaker_audio(row[speakerI], str(line_number), row[wordI])
            check_timestamp_audio(row[timestampI], str(line_number), row[wordI])
            if len(row) > 6:
                check_basic_level_audio(row[basicI], str(line_number), row[wordI])
        line_number += 1
    return error_log

def give_error_report(filepath):
    info = []
    with open(filepath, 'rt') as csvfileR:
        reader = csv.reader(csvfileR)
        for row in reader:
            info.append(row)

    if "word" in info[0]:
        error_log = give_error_report_audio(info)
    else:
        error_log = give_error_report_video(info)

    return error_log


