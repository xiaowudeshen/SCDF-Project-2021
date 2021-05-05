# Author: Victor Li
# Date: 5/5/21
# Version:5:29
# mainly designed to check and read the annotation
# Add more features in checking the incidence name, question and answers

from os import listdir
from os.path import isfile, join
import re
import argparse
import string




parser = argparse.ArgumentParser()
parser.add_argument("-path", default= 'test', help='path to the directory where all the annotated data is stored')
parser.add_argument("-name", default= 'student' ,help='Name of the annotator')
args = parser.parse_args()



#### Change this file
DATA_DIRECTORY = args.path
###
OUTPUT1 = 'Output1'
# OUTPUT2 = 'Output2'
Speaker_dic = {}
Channel_dic = {}

conv = []
ann = []
name = []
gen =[]
age = []
phone = []
address = []
inc = {}

global file_list, data_dic, file_dic, turn_dic, turn_list, final_list

data_dic = {}
file_dic = {}
turn_dic = {}
file_list = []
turn_list = []
final_list = []

inc_dic =  {'ABDOMINAL PAIN': {'respond usual way': ' Yes || No  (i.e. not alert) || Unknown', 'faint': ' Yes || No / Unknown || Not Applicable', 'pregnant': ' Yes || No / Unknown || Not Applicable', 'vomiting look': ' No || Blood / Coffee-ground || Others', 'passing motion': ' Yes || No (Black / Sticky / Blood) || No (Diarrhea / Constipate) / Unknow'}, 'allergies/stings': {'Where': ' Nearby || Unknown || Not Applicable', 'respond usual way': ' Yes || No (i.e. not alert) || Unknown', 'difficulty breathing swallowing': ' Yes || No || Unknown', 'history severe': ' Yes || No / Unknown || Not Applicable', 'How long': ' Less than 1 hour / Unknown (3rd party) || More than 1 hour || More than 1 da'}, 'animal bite/attack': {'kind animal': ' Insect, spider or snake || Large/EXOTIC animal || Others', 'Where now': ' Nearby || Unknown', 'respond usual way': ' Yes || No (i.e. not alert) || Unknown', 'blood': ' Yes || No / Unknow', 'stopped how much loss': ' No. More than 1 cup || No. Less than 1 cup || Yes', 'part of the body': ' Central body || Peripheral limbs || Unknown'}, 'assault/rape': {'weapons': ' Yes || No', 'respond usual way': ' Yes || No (i.e. not alert) || Unknown', 'blood': ' Yes|| No / Unknow', 'stopped how much loss': ' No. More than 1 cup || No. Less than 1 cup || Yes', 'part of the body': ' Central body || Peripheral limbs || Unknown'}, 'Back Pain': {'when start': ' Less than 6 hour || More than 6 hou', 'what caused the back pain': ' Recent Fall || Recent Trauma || Unknown || Not Applicabl', 'chest pain': ' Yes || No || Not Applicabl', 'respond usual way': ' Yes || No || Unknow', 'faint': ' Yes || No / Unknown || No / Unknown (non-recent'}, 'Bleeding/Laceration': {'bleeding from': ' Amputation || Vagina || Nosebleed || Other', 'pregnant': ' Yes || No || Not Applicabl', 'respond usual way': ' Yes || No || Unknow', 'bleeding stopped? how much loss?': ' No. More than 1cup || No. Less than 1cup || Ye', 'disorder or blood thinners': ' Yes || No / Unknow', 'vomiting / coughing blood': ' Vomiting blood || Coughing blood || No / Unknow', 'part of the body': ' Central body || Peripheral limbs || Unknow'}, 'Breathing Problem': {'choking': ' Yes || No / Unknow', 'respond usual way': ' Yes || No || Unknown / Not Applicabl', 'full sentence or one word': ' One/few words || Full sentence || Not Applicabl', 'coughing blood': ' Yes || No / Unknow', 'asthma lung disease': ' Yes || No / Unknow'}, 'Burns': {'safe out of danger': ' Yes || N', 'burned/injured': ' Electrical || Explosion || Heat/Fire || Household/Chemica', 'respond usual way': ' Yes || No || Unknow', 'difficulty breathing': ' Yes || No / Unknow', 'full sentence or one word': ' One/few words || Full Sentence || Not Applicabl', 'part burned/injured': ' Facial || 15% body area or more || Less than 15% body area || Sunburn / Less than hand size || Unknow'}, 'Cardiac Arrest / Death': {'why dead': 'OBVIOUS Death ||EXPECTED Death ||Not Breathing ||Uncertain Breathing ||Hanging ||Strangulation ||Suffocation ||INEFFECTIVE BREATHING from other Protocol', 'try resuscitate': 'Yes ||Uncertain ||Not Applicable', 'advised could happen': 'Yes ||Uncertain ||Not Applicable', 'Where': 'Still Hanging ||On the floor ||Others', 'bring down': 'Yes ||No / Not accessible'}, 'Chest / Heart Pain': {'respond usual way': 'Yes || No || Unknown', 'full sentence one word': 'Few words || Full Sentence || Unknown', 'pale AND cold sweat': 'Yes || No / Unknown', 'pacemaker': 'Yes || No / Unknown', 'discharge': 'Yes || No || Not Applicable', 'heart attack similar episode': 'Yes ||Slow / Fast heart rate / SVT / VT ||No ||Unknown'}, 'Childbirth / Obstetrics': {'weeks pregnant': '1st Trimester ||2nd Trimester ||3rd Trimester', 'contractions': 'Yes ||No ||Unknown', 'see part': 'No || BREECH or CORD || Head visible/out ||Baby born ||Not Applicable', 'first': 'Yes ||No ||Not Applicable', 'minutes apart': '2 minutes or less apart ||5 minutes or less apart ||More than 5 minutes apart ||Unknown ||Not Applicable', 'bleeding': 'Yes ||No ||Unknown'}, 'CHOKING': {'choke': 'Liquids ||Solids', 'coughing': 'No (Unconscious) ||No (Conscious) ||Yes', 'talk normally': 'No ||Yes'}, 'CONVULSIONS / FITS': {'jerking stopped': 'Stopped || Still jerking || Unknow', 'breathing': ' Not breathing || Breathing || Unknow', 'more than one': ' Multiple episode || One episode || Unknow', 'respond usual way': ' Yes || No || Unknow', 'pregnant': ' Pregnant || Not pregnant || Not Applicabl', 'fever': ' Fever || No fever / Unknown || Not Applicabl', 'history diabetes': ' Diabetic || Unknown || No diabete'}, 'DIABETIC PROBLEM': {'respond usual way': ' Yes || No || Unknow', 'breathing normal': ' No || Ye', 'full sentence few words': ' Few words || Full Sentence || Not Applicabl', 'behaving normally': ' Combative || Yes || Giddy / Drows', 'eaten': ' Yes || N'}, 'DIVING / DROWNING': {'Where now': ' In water || Out of water || Unknow', 'respond usual way': ' Unconscious || Not alert || Yes || Unknow', 'breathing normal': ' No AND Unconscious || No || Ye', 'injuries': ' Yes (DIVING / SCUBA) || Yes (Others) || Unknown || N'}, 'ELECTROCUTIONS': {'disconnected source': ' Yes || No / Unknow', 'respond usual way': ' Unconscious & breathing || No (i.e. not alert) || Yes || Unknow', 'breathing normal pace': ' No || Yes || Unknow', 'full sentence few words': ' Few words || Full Sentence || Not Applicabl', 'fall yes, how far': ' 2m and above  || Less than 2m / 6ft || Unknown (3rd party)  || N'}, 'Eye Problem': {'respond usual way': ' Yes || No || Unknow', 'How happen': ' Direct blow || Flying object || Penetrating object || Chemical || Small foreign object || Welding || Contact lens || MEDICAL eye proble'}, 'FAllS/BACK Injury': {'caused': ' Dizziness with fall || Electrocution / Lightning ||Fainted / Nearly fainted ||Jumped || Accidental / Unknow', 'far fall': ' More than 9m / 3 storey || 2m and above || Less than 2m / 6ft || Unknow', 'respond usual way': ' Yes || No || Unknow', 'difficulty breathing': ' Yes || No || Unknow', 'blood': ' Yes || N', 'difficulty walking': ' Yes || No/Unknow', 'part of body': ' Central body || Peripheral limbs || unknown || no injur'}, 'Giddy/Headache': {'respond usual way': ' Yes|| No || Unknow', 'severe': ' Yes || No || Unknow', 'numbness paralysis': ' No || Numbness || Paralysis || Unknow', 'change behavior': ' Yes || No || Unknow'}, 'Heat/Cold exposure': {'respond usual way': ' Yes || No || Unknow', 'breathing normal': ' No || Yes || Unknow', 'full sentence or one word': ' One/few words || full sentence || not applicabl', 'skin feel': ' Colder than normal || hotter than normal || normal || unknow'}, 'INHALATION': {'safe out of danger': ' Yes || No / Unknow', 'chemicals/fumes  involved': ' Chemical || Carbon Monoxide || Gas (methane) || Unknow', 'respond usual way': ' Unconscious || No || Yes || Unknow', 'difficulty breathing': ' Yes AND Unconscious || Yes || No || Unknow'}, 'MOTOR VEHICLE ACCIDENT': {'vehicle involved': ' Multiple\tvehicle || Rollover / Overturned || Vehicle Bicycle || Vehicle Pedestrian || Vehicle Terrain || Vehicle Motorcycle || Vehicle Vehicle || Vehicle Animal / Personal Mobility Device Pedestrian || Single vehicle (skidded', 'trapped': ' Yes || No || Unknow', 'thrown': ' Yes || No || Unknow', 'everyone able talk': ' Yes || No || Unknow', 'obvious': ' Yes / Unknown || N', 'blood': ' Yes || N'}, 'POISONING/INGESTION': {'What \ttake': ' Antidepressants|| Acid or Alkali || Cocaine || Narcotics || Over\tthe\tCounter drugs || Alcohol Intoxication || Unknow', 'weapon': ' Yes || N', 'respond usual way': ' Yes || No || Unknow', 'attempt': ' Jumper || Carbon monoxide || Overdose || Stab or Gunshot wound || THREATENING SUICIDE || Laceration / Cut || No || Unknow', 'blood': ' Yes || N'}, 'PSYCHIATRIC / BEHAVIORAL': {'violent': ' Yes || No || Unknow', 'weapon': ' Yes || N', 'respond usual way': ' Yes || No (i.e. not alert) || Unknow', 'attempt': ' Jumper || Carbon monoxide || Overdose || Stab or Gunshot wound || THREATENING SUICIDE || Laceration / Cut || No || Unknow', 'blood': ' Yes || No / Unknow'}, 'sick person (specific diagnosis)': {'difficulty breathing': ' yes || no || unknow', 'chest pain': ' yes || no || unknow', 'bleeding vomiting blood': 'Yes || No || Unknow', 'respond usual way': 'No || Yes/Unknow', 'difficulty walking': 'Yes || Unknown || N'}, 'stab/gunshot injury(penetrating)': {'assailant': 'Yes. One assailant || Yes. More than one assailant || N', 'resuscitate': 'Yes || Unconsciousor ARREST || Not Applicable', 'respond usual way': 'Yes || No || Unknow', 'part injured': ' CENTRAL wounds || PERIPHERAL wound', 'morethan one wound': 'Yes || No || Unknow'}, 'STROKE/ CVA': {'respond usual way': ' YES || NO || UNKNOW', 'STROKE0': ' None || Slurred Speech || Weakness / Numbness || Paralysis / Facial droop||Movement problems||Vision problems||Sudden onset of severe headache||Unknow', 'what time start': ' Less than3 hours || More than 3 hour', 'STROKE': 'YES||NO||UNKNOW'}, 'TRAUMATIC INJURIES': {'respond usual way': 'Unconscious & breathing (per Case Entry)||No||Yes||Unknow', 'released': 'No||Yes||Not Applicabl', 'part of the body': 'CENTRAL body||PERIPHERAL limbs||Unknown', 'parts been found': 'Yes (Amputation CC at end of Question)||No / Unknown||Not Applicabl', 'broken bones': 'Yes || No|| Unknow', 'blood': 'YES||NO||Unknow'}, 'Unconscious/fainting': {'UNCONSCIOUS & NO/UNCERTAIN': ' No || Yes || Not applicabl', 'respond usual way': ' Yes || No || Unknow', 'breathing normal': ' No || Yes || Unknow', 'full sentence or one word': ' One/few words || full sentence || not applicabl', 'history heart problem': ' Yes || No ||unknow', 'abdominal': ' Yes || No || not applicabl', 'more than once': ' Yes || No || Unknow'}, 'Unknown': {'respond usual way': ' Yes || No || Unknown || Language Barrie', 'talk': ' Yes || No || Unknow', 'standing, sitting, lying': ' standing || sitting || lying || unknow', 'moving': ' Yes || No/unknow'}}

# inc_dic =  {'ABDOMINAL PAIN': {'respond usual way': ' Yes || No  (i.e. not alert) || UnknownP1 ', 'faint': ' Yes || No / Unknown || Not Applicable ', 'pregnant': ' Yes || No / Unknown || Not Applicable ', 'vomiting look': ' No || Blood / Coffee-ground || Others ', 'passingmotion': ' Yes || No (Black / Sticky / Blood) || No (Diarrhea / Constipate) / Unknown'}, 'allergies/stings': {'Where': ' Nearby || Unknown || Not Applicable ', 'respond usual way': ' Yes || No (i.e. not alert) || Unknown ', 'difficulty breathing swallowing': ' Yes || No || Unknown ', 'history SEVERE': ' Yes || No / Unknown || Not Applicable ', 'How long': ' Lessthan 1 hour / Unknown (3rdparty) || More than 1 hour || More than 1 day'}, 'animal bite/attack': {'kind animal': ' Insect,spideror snake || Large/EXOTICanima || Others ', 'Where now': ' Nearby || Unknown ', 'respond usual way': ' Yes || No (i.e. not alert) || Unknown ', 'blood': ' Yes || No / Unknown', 'stopped how much loss': ' No. More than 1 cup || No. Less than 1 cup || Yes ', 'part of the body': ' CENTRALbody || PERIPHERALlimbs || Unknown '}, 'assault/rape': {'weapons': ' Yes || No ', 'respond usual way': ' Yes || No (i.e. not alert) || Unknown ', 'blood': ' Yes|| No / Unknown', 'stopped how much loss': ' No. More than 1 cup || No. Less than 1 cup || Yes ', 'part of the body': ' CENTRALbody || PERIPHERALlimbs || Unknown '}, 'Back Pain': {'when start': ' Less than 6 hour || More than 6 hour', 'what caused the back pain': ' Recent Fall || Recent Trauma || Unknown || Not Applicable', 'chest pain': ' Yes || No || Not Applicable', 'respond usual way': ' Yes || No || Unknown', 'faint': ' Yes || No / Unknown || No / Unknown (non-recent)'}, 'Bleeding/Laceration': {'bleeding from': ' Amputation || Vagina || Nosebleed || Others', 'pregnant': ' Yes || No || Not Applicable', 'respond usual way': ' Yes || No || Unknown', 'bleeding stopped? how much loss?': ' No. More than 1cup || No. Less than 1cup || Yes', 'bleeding disorder or blood thinners': ' Yes || No / Unknown', 'vomiting / coughing blood': ' Vomiting blood || Coughing blood || No / Unknown', 'part of the body': ' Central body || Peripheral limbs || Unknown'}, 'Breathing Problem': {'choking': ' Yes || No / Unknown', 'respond usual way': ' Yes || No || Unknown / Not Applicable', 'full sentence or one word': ' One/few words || Full sentence || Not Applicable', 'coughing blood': ' Yes || No / Unknown', 'asthma lung disease': ' Yes || No / Unknown'}, 'Burns': {'safe out of danger': ' Yes || No', 'burned/injured': ' Electrical || Explosion || Heat/Fire || Household/Chemical', 'respond usual way': ' Yes || No || Unknown', 'difficulty breathing': ' Yes || No / Unknown', 'full sentence or one word': ' One/few words || Full Sentence || Not Applicable', 'part burned/injured': ' Facial || 15% body area or more || Less than 15% body area || Sunburn / Less than hand size || Unknown'}, '9.Cardiac Arrest / Death': {'why dead': 'OBVIOUS Death ||EXPECTED Death ||Not Breathing ||Uncertain Breathing ||Hanging ||Strangulation ||Suffocation ||INEFFECTIVE BREATHING from other Protocol ', 'try resuscitate': 'Yes ||Uncertain ||Not Applicable ', 'advised could happen': 'Yes ||Uncertain ||Not Applicable ', 'Where': 'Still Hanging ||On the floor ||Others ', 'bring down': 'Yes ||No / Not accessible '}, '10.Chest / Heart Pain': {'respond usual way': 'Yes || No || Unknown ', 'full sentence one word': 'Few words || Full Sentence || Unknown ', 'pale AND cold sweat': 'Yes || No / Unknown ', 'pacemaker': 'Yes || No / Unknown ', 'discharge': 'Yes || No || Not Applicable ', 'heart attack similar episode': 'Yes ||Slow / Fast heart rate / SVT / VT ||No ||Unknown '}, '11.Childbirth / Obstetrics': {'weeks pregnant': '1st Trimester ||2nd Trimester ||3rd Trimester ', 'contractions': 'Yes ||No ||Unknown ', 'see part': 'No || BREECH or CORD || Head visible/out ||Baby born ||Not Applicable ', 'first': 'Yes ||No ||Not Applicable ', 'minutes apart': '2 minutes or less apart ||5 minutes or less apart ||More than 5 minutes apart ||Unknown ||Not Applicable ', 'bleeding': 'Yes ||No ||Unknown '}, 'CHOKING': {'choke': 'Liquids ||Solids ', 'coughing': 'No (Unconscious) ||No (Conscious) ||Yes ', 'talk normally': 'No ||Yes '}, 'CONVULSIONS / FITS': {'jerking stopped': 'Stopped || Still jerking || Unknown', 'breathing': ' Not breathing || Breathing || Unknown', 'more than one': ' Multiple episode || One episode || Unknown', 'respond usual way': ' Yes || No || Unknown', 'pregnant': ' Pregnant || Not pregnant || Not Applicable', 'fever': ' Fever || No fever / Unknown || Not Applicable', 'history diabetes': ' Diabetic || Unknown || No diabetes'}, 'DIABETIC PROBLEM': {'respond usual way': ' Yes || No || Unknown', 'breathing normal': ' No || Yes', 'full sentence few words': ' Few words || Full Sentence || Not Applicable', 'behaving normally': ' Combative || Yes || Giddy / Drowsy', 'eaten': ' Yes || No'}, 'DIVING / DROWNING': {'Where now': ' In water || Out of water || Unknown', 'respond usual way': ' Unconscious || Not alert || Yes || Unknown', 'breathing normal': ' No AND Unconscious || No || Yes', 'injuries': ' Yes (DIVING / SCUBA) || Yes (Others) || Unknown || No'}, 'ELECTROCUTIONS': {'disconnected source': ' Yes || No / Unknown', 'respond usual way': ' Unconscious & breathing || No (i.e. not alert) || Yes || Unknown', 'breathing normal pace': ' No || Yes || Unknown', 'full sentence few words': ' Few words || Full Sentence || Not Applicable', 'fall yes, how far': ' 2m and above  || Less than 2m / 6ft || Unknown (3rd party)  || No'}, 'Eye Problem:': {'respond usual way': ' Yes || No || Unknown', 'How happen': ' Direct blow || Flying object || Penetrating object || Chemical || Small foreign object || Welding || Contact lens || MEDICAL eye problem'}, 'FAllS/BACK Injury': {'caused': ' Dizziness with fall || Electrocution / Lightning ||Fainted / Nearly fainted ||Jumped || Accidental / Unknown', 'far fall': ' More than 9m / 3 storey || 2m and above || Less than 2m / 6ft || Unknown', 'respond usual way': ' Yes || No || Unknown', 'difficulty breathing': ' Yes || No || Unknown', 'blood': ' Yes || No', 'difficulty walking': ' Yes || No/Unknown', 'part of body': ' Central body || Peripheral limbs || unknown || no injury'}, 'Giddy/Headache': {'respond usual way': ' Yes|| No || Unknown', 'severe': ' Yes || No || Unknown', 'numbness paralysis': ' No || Numbness || Paralysis || Unknown', 'change behavior': ' Yes || No || Unknown'}, 'Heat/Cold exposure': {'respond usual way': ' Yes || No || Unknown', 'breathing normal': ' No || Yes || Unknown', 'full sentence or one word': ' One/few words || full sentence || not applicable', 'skin feel': ' Colder than normal || hotter than normal || normal || unknown'}, 'INHALATION': {'safe out of danger': ' Yes || No / Unknown', 'chemicals/fumes  involved': ' Chemical || Carbon Monoxide || Gas (methane) || Unknown', 'respond usual way': ' Unconscious || No || Yes || Unknown', 'difficulty\tbreathing': ' Yes\tAND Unconscious || Yes || No || Unknown'}, 'MOTOR VEHICLE ACCIDENT': {'vehicle involved': ' Multiple\tvehicle || Rollover\t/\tOverturned\t|| Vehicle Bicycle || Vehicle Pedestrian || Vehicle Terrain || Vehicle Motorcycle || Vehicle Vehicle || Vehicle Animal\t/\tPersonal\tMobility\tDevice Pedestrian || Single vehicle (skidded)', 'trapped': ' Yes || No || Unknown', 'thrown': ' Yes || No || Unknown', 'everyone able talk': ' Yes || No || Unknown', 'obvious': ' Yes\t/\tUnknown || No', 'blood': ' Yes || No'}, 'POISONING/INGESTION': {'What \ttake': ' Antidepressants|| Acid or Alkali || Cocaine || Narcotics || Over\tthe\tCounter drugs || Alcohol Intoxication || Unknown', 'weapon': ' Yes || No', 'respond usual way': ' Yes || No || Unknown', 'attempt': ' Jumper || Carbon monoxide || Overdose || Stab or Gunshot wound || THREATENING SUICIDE || Laceration / Cut || No || Unknown', 'blood': ' Yes || No'}, 'PSYCHIATRIC / BEHAVIORAL': {'violent': ' Yes || No || Unknown', 'weapon': ' Yes || No', 'respond usual way': ' Yes || No (i.e. not alert) || Unknown', 'attempt': ' Jumper || Carbon monoxide || Overdose || Stab or Gunshot wound || THREATENING SUICIDE || Laceration / Cut || No || Unknown', 'blood': ' Yes || No / Unknown'}, 'sick person (specific diagnosis)': {'difficulty breathing': ' yes || no || unknown', 'chest pain': ' yes || no || unknown', 'bleeding vomiting blood': 'Yes || No || Unknown', 'respond usual way': 'No || Yes/Unknown', 'difficulty walking': 'Yes || Unknown || No'}, 'stab/gunshot injury(penetrating)': {'assailant': 'Yes. One assailant || Yes. More than one assailant || No', 'resuscitate': 'Yes || Unconsciousor ARREST || Not Applicable ', 'respond usual way': 'Yes || No || Unknown', 'part injured': ' CENTRAL wounds || PERIPHERAL wounds', 'morethan one wound': 'Yes || No || Unknown'}, 'STROKE/ CVA': {'respond usual way': ' YES || NO || UNKNOWN', 'STROKE': 'YES||NO||UNKNOWN', 'what time start': ' Less than3 hours || More than 3 hours'}, 'TRAUMATIC INJURIES': {'respond usual way': 'Unconscious & breathing (per Case Entry)||No||Yes||Unknown', 'released': 'No||Yes||Not Applicable', 'part of the body': 'CENTRALbody||PERIPHERALlimbs||Unknown ', 'parts been found': 'Yes (Amputation CC at end of Question)||No / Unknown||Not Applicable', 'broken bones': 'Yes || No|| Unknown', 'blood': 'YES||NO||Unknown'}, 'Unconscious/fainting': {'UNCONSCIOUS & NO/UNCERTAIN': ' No || Yes || Not applicable', 'respond usual way': ' Yes || No || Unknown', 'breathing normal': ' No || Yes || Unknown', 'full sentence or one word': ' One/few words || full sentence || not applicable', 'history heart problem': ' Yes || No ||unknown', 'abdominal': ' Yes || No || not applicable', 'more than once': ' Yes || No || Unknown'}, 'Unknown': {'respond usual way': ' Yes || No || Unknown || Language Barrier', 'talk': ' Yes || No || Unknown', 'standing, sitting, lying': ' standing || sitting || lying || unknown', 'moving': ' Yes || No/unknow'}}
## store number of terms of conv and number of tag pairs in each dialogue file
num_conv = []
num_tag = []


def write_to_output(dic, file, mess):
    # file = open(join(dic, file), 'w+')
    # with open(join(dic, file), 'a+') as the_file:
    #     for m in mess:
    #         the_file.write(join(m+'|'))
    #
    #     the_file.write('\n')
    pass

def is_inc(inc_name):
    if inc_name in inc_dic:
        return True
    else:
        raise Exception("incidence is not in the list. Incidence Name:", inc_name)
        
    
def is_question(inc_name, pre_ques):
    q1 = pre_ques[1:-1].split("; ")
    result = 0
    for q in q1:
        ques = q.split(":")
        if ques[0].strip()[1:-1] in inc_dic[inc_name]:
            ans = inc_dic[inc_name][ques[0].strip()[1:-1]].split('||')
            print(ans)
            for index, aa in enumerate(ans):
                ans[index] = aa.strip()
            ques1 = ques[1].strip()
            if ques1 in ans:
                result = 1
            else:
                print(ques1, ans)
                raise Exception("Ans name not in the list, Incidence and Question", inc_name, ques)
        elif ques == [' '] or ques == ['']:
            result = 0
        else:
            a = 1
            raise Exception("question name not in the list. Incidence and Question Name:", inc_name, ques)

        if result == 1:
            return True
        else:
            return False
    
def write_inc(inc, inc_name, pre_ques):
    q1 = pre_ques[1:-2].split("; ")
    for q in q1:
        ques = q.split(":")
        # print(ques[0].strip()[1:-1])
        if inc_name in inc:

            tmp_dic = inc[inc_name]

        else:
            tmp_dic = {}
        # print(ques[0].strip()[1:-1])
        tmp_dic[ques[0].strip()[1:-1]] = ques[1]
        inc[inc_name] = tmp_dic
    return inc
    
    
def replace_list(mlist, item, new_item):
    for index, m in enumerate(mlist):
        if m == item:
            mlist[index] = new_item

    return mlist


def read_ann(sentence, name, age, gen, phone, address, inc):
    global inc_list
    # return the annaotated tag pari information
    if len(sentence[2].strip()) == 3:

        if sentence[2] == 'per':
            name.append(sentence[1])
        elif sentence[2] == 'gen':
            gen.append(sentence[1])
        elif sentence[2] == 'age':
            age.append(sentence[1])
        elif sentence[2] == 'num':
            phone.append(sentence[1])
        elif sentence[2] == 'loc':
            address.append(sentence[1])
        elif sentence[2] == 'inc':
            if is_inc(sentence[1]) and is_question(sentence[1], sentence[3]):
                inc = write_inc(inc, sentence[1], sentence[3])
    elif not (re.findall('\((.*?)\)', sentence[2]) == '*'):
        content = re.findall('\((.*?)\)', sentence[2])
        new_content = sentence[1]
        if sentence[2].startswith('per'):
            name = replace_list(name, content, new_content)
        elif sentence[2].startswith('gen'):
            gen = replace_list(gen, content, new_content)
        elif sentence[2].startswith('age'):
            age = replace_list(age, content, new_content)
        elif sentence[2].startswith('num'):
            phone = replace_list(phone, content, new_content)
        elif sentence[2].startswith('loc'):
            address = replace_list(address, content, new_content)
        elif sentence[2].startswith('inc'):
            if is_inc(sentence[1]) and is_question(sentence[1], sentence[3]):
                inc = write_inc(inc, sentence[1], sentence[3])
    inc_list = []
    inc_list.append(inc)
    ann = ['<Name>:'] + name + ['<Age>'] + age +['<Gender>'] + gen + ['<Phone>'] + phone + ['<Address>'] + address + ['<Incidence>'] + inc_list
    print(ann)
    return ann


def read_conv(lines, conv, ann):
    turn_dic = {}
    turn_idx = 0
    ans_flag = 1
    for index, line in enumerate(lines[2:]):
        # print(line)
        if line.strip():
            message = line[:-1].split('\t')
            # print(message)
            if ans_flag and message[0] == Channel_dic['operator']:
                conv.append('<operator>')
                conv.append(message[3])
                # print(conv)
            elif message[0] == Channel_dic['caller']:
                conv.append('<caller>')
                conv.append(message[3])
                ans_flag = 0
            # elif message[0] == 'tag pair ' and not (index == len(lines[2:])):
            elif message[0] == 'tag pair ':
                ann = read_ann(message, name, age, gen, phone, address, inc)
            elif message[0] == Channel_dic['operator'] or message[0].startswith('priority list'):
                if message[0].startswith('priority list'):
                    priority = message[1]


                turn_dic['turn_idx'] = turn_idx
                turn_dic['Turn_conv'] = conv
                turn_dic['Turn_tag'] = ann
                turn_dic_cur = turn_dic.copy()
                turn_list.append(turn_dic_cur)
                turn_idx +=1
                # write_to_output(OUTPUT1, file, conv)
                # write_to_output(OUTPUT2, file, ann)


                conv = []
                if message[0] == Channel_dic['operator']:
                    conv.append('<operator>')
                    conv.append(message[3])
                    ans_flag = 1
    # conv ends by the operator, print result to output file
    if conv:
        # write_to_output(OUTPUT1, file, conv)
        turn_dic['turn_idx'] = turn_idx
        turn_dic['Turn_conv'] = conv
        turn_dic['Turn_tag'] = ann
        turn_dic_cur = turn_dic.copy()
        turn_list.append(turn_dic_cur)
        turn_idx += 1

    return priority




ann_files = [f for f in listdir(DATA_DIRECTORY) if isfile(join(DATA_DIRECTORY, f)) and f[0] != '.']
# print(ann_files)

for file in ann_files:
    conv = []
    ann = []
    name = []
    gen = []
    age = []
    phone = []
    address = []
    inc = {}
    inc_list = []
    file_dic = {}
    turn_list = []
    print('processing file name'+ file)
    file_dic['File_idx'] = file
    read_header = 1
    # clear output file
    # with open(join(OUTPUT1, file), 'w+') as the_file:
    #     the_file.write('Ready to write all the information about the dialogue\n')
    # with open(join(OUTPUT2, file), 'w+') as the_file:
    #     the_file.write('Ready to write all the information about the content\n')
    with open(join(DATA_DIRECTORY, file), 'r') as the_file:
        count = -1
        lines = the_file.readlines()
        if read_header:
            # check if the speakers are well defined
            if ' = ' in lines[0]:
                message = lines[0].split(' = ')
            elif '=' in lines[0]:
                message = lines[0].split('=')
            else:
                raise Exception("Syntax error when defining speaker role in file", file)


            # print(message)
            if not (len(message) == 2):
                raise Exception("Not define speaker roles in file", file)
            Speaker_dic[message[0]] = message[1].rstrip()

            if ' = ' in lines[1]:
                message = lines[1].split(' = ')
            elif '=' in lines[1]:
                message = lines[1].split('=')
            else:
                raise Exception("Syntax error when defining speaker role in file", file)

            if not (len(message) == 2):
                raise Exception("Not define speaker roles in file", file)
            Speaker_dic[message[0]] = message[1].rstrip()
            # print(Speaker_dic)
            read_header = 0
            Channel_dic = {v: k for k, v in Speaker_dic.items()}
            #check if empty line between
            if lines[2].strip():
                raise Exception("No empty space between indicator and conversation in file", file)

            # check if the operator starts the dialogue
            message = lines[3].split('\t')
            # print(message)
            if not (Speaker_dic[message[0]].startswith('operator')):
                raise Exception("Conversation is not started by the operator in file", file)

            while not lines[count].strip():
                count -= 1
            message = lines[count].split('\t')
            if not message[0].startswith('priority list'):
                raise Exception("Conversation is not finished with priority list in file", file)


        print('Ready to read file name:' + file)
        pri = read_conv(lines, conv, ann)
        file_dic['Dialogue_turn'] = turn_list
        file_dic['priority_list'] = pri
        print('finish reading file name:' + file)
    file_list.append(file_dic)

data_dic['DATA_idx'] = args.name
data_dic['Files'] = file_list
final_list.append(data_dic)
print(final_list)
print('++++MISSION COMPLETE++++')
