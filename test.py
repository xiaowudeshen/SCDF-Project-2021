import re
import ast

# file = open("inc_description_all.txt", "r")
inc_dic = {}
q = 1
with open("inc_list_all.txt") as f:
    for line in f:
        if line.strip():
            if not line.startswith("{"):
                # print(line)
                # break
                if not q:
                    inc_dic[inc_name] = q_dic
                    q = 1
                q_dic = {}
                message =line[:-1].split(". ")
                inc_name = message[-1]
            else:
                q = 0
                # print(line)
                (key, val) = line[1:-2].split(":")
                q_dic[key[1:-1]] = val
        if not q:
            inc_dic[inc_name] = q_dic

#
#
# # inc_dic = {'ABDOMINAL PAIN': {'"respond usual way"': ' Yes || No  (i.e. not alert) || UnknownP1 }', '"faint"': ' Yes || No / Unknown || Not Applicable }', '"pregnant"': ' Yes || No / Unknown || Not Applicable }', '"vomiting look"': ' No || Blood / Coffee-ground || Others }', '"passingmotion"': ' Yes || No (Black / Sticky / Blood) || No (Diarrhea / Constipate) / Unknown}'}, 'allergies/stings': {'"Where"': ' Nearby || Unknown || Not Applicable }', '"respond usual way"': ' Yes || No (i.e. not alert) || Unknown }', '"difficulty breathing swallowing"': ' Yes || No || Unknown }', '"history SEVERE"': ' Yes || No / Unknown || Not Applicable }', '"How long"': ' Lessthan 1 hour / Unknown (3rdparty) || More than 1 hour || More than 1 day}'}, 'animal bite/attack': {'"kind animal"': ' Insect,spideror snake || Large/EXOTICanima || Others }', '"Where now"': ' Nearby || Unknown }', '"respond usual way"': ' Yes || No (i.e. not alert) || Unknown }', '"blood"': ' Yes || No / Unknown}', '"stopped how much loss"': ' No. More than 1 cup || No. Less than 1 cup || Yes }', '"part of the body"': ' CENTRALbody || PERIPHERALlimbs || Unknown }'}, 'assault/rape': {'"weapons"': ' Yes || No }', '"respond usual way"': ' Yes || No (i.e. not alert) || Unknown }', '"blood"': ' Yes|| No / Unknown}', '"stopped how much loss"': ' No. More than 1 cup || No. Less than 1 cup || Yes }', '"part of the body"': ' CENTRALbody || PERIPHERALlimbs || Unknown }'}, 'Back Pain:': {'"when start"': ' Less than 6 hour || More than 6 hour}', '"what caused the back pain"': ' Recent Fall || Recent Trauma || Unknown || Not Applicable}', '"chest pain"': ' Yes || No || Not Applicable}', '"respond usual way"': ' Yes || No || Unknown}', '"faint"': ' Yes || No / Unknown || No / Unknown (non-recent)}'}, 'Bleeding/Laceration:': {'"bleeding from"': ' Amputation || Vagina || Nosebleed || Others}', '"pregnant"': ' Yes || No || Not Applicable}', '"respond usual way"': ' Yes || No || Unknown}', '"bleeding stopped? how much loss?"': ' No. More than 1cup || No. Less than 1cup || Yes}', '"bleeding disorder or blood thinners"': ' Yes || No / Unknown}', '"vomiting / coughing blood"': ' Vomiting blood || Coughing blood || No / Unknown}', '"part of the body"': ' Central body || Peripheral limbs || Unknown}'}, 'Breathing Problem:': {'"choking"': ' Yes || No / Unknown}', '"respond usual way"': ' Yes || No || Unknown / Not Applicable}', '"full sentence or one word"': ' One/few words || Full sentence || Not Applicable}', '"coughing blood"': ' Yes || No / Unknown}', '"asthma lung disease"': ' Yes || No / Unknown}'}, 'Burns:': {'"safe out of danger"': ' Yes || No}', '"burned/injured"': ' Electrical || Explosion || Heat/Fire || Household/Chemical}', '"respond usual way"': ' Yes || No || Unknown}', '"difficulty breathing"': ' Yes || No / Unknown}', '"full sentence or one word"': ' One/few words || Full Sentence || Not Applicable}', '"part burned/injured"': ' Facial || 15% body area or more || Less than 15% body area || Sunburn / Less than hand size || Unknown}'}, 'CONVULSIONS / FITS': {'"jerking stopped"': 'Stopped || Still jerking || Unknown}', '"breathing"': ' Not breathing || Breathing || Unknown}', '"more than one"': ' Multiple episode || One episode || Unknown}', '"respond usual way"': ' Yes || No || Unknown}', '"pregnant"': ' Pregnant || Not pregnant || Not Applicable}', '"fever"': ' Fever || No fever / Unknown || Not Applicable}', '"history diabetes"': ' Diabetic || Unknown || No diabetes}'}, 'DIABETIC PROBLEM': {'"respond usual way"': ' Yes || No || Unknown}', '"breathing normal"': ' No || Yes}', '"full sentence few words"': ' Few words || Full Sentence || Not Applicable}', '"behaving normally"': ' Combative || Yes || Giddy / Drowsy}', '"eaten"': ' Yes || No}'}, 'DIVING / DROWNING': {'"Where now"': ' In water || Out of water || Unknown}', '"respond usual way"': ' Unconscious || Not alert || Yes || Unknown}', '"breathing normal"': ' No AND Unconscious || No || Yes}', '"injuries"': ' Yes (DIVING / SCUBA) || Yes (Others) || Unknown || No}'}, 'ELECTROCUTIONS': {'"disconnected source"': ' Yes || No / Unknown}', '"respond usual way"': ' Unconscious & breathing || No (i.e. not alert) || Yes || Unknown}', '"breathing normal pace"': ' No || Yes || Unknown}', '"full sentence few words"': ' Few words || Full Sentence || Not Applicable}', '"fall yes, how far"': ' 2m and above  || Less than 2m / 6ft || Unknown (3rd party)  || No}'}, 'Eye Problem:': {'"respond usual way"': ' Yes || No || Unknown}', '"How happen"': ' Direct blow || Flying object || Penetrating object || Chemical || Small foreign object || Welding || Contact lens || MEDICAL eye problem}'}, 'FAllS/BACK Injury:': {'"caused"': ' Dizziness with fall || Electrocution / Lightning ||Fainted / Nearly fainted ||Jumped || Accidental / Unknown}', '"far fall"': ' More than 9m / 3 storey || 2m and above || Less than 2m / 6ft || Unknown}', '"respond usual way"': ' Yes || No || Unknown}', '"difficulty breathing"': ' Yes || No || Unknown}', '"blood"': ' Yes || No}', '"difficulty walking"': ' Yes || No/Unknown}', '"part of body"': ' Central body || Peripheral limbs || unknown || no injury}'}, 'Giddy/Headache:': {'"respond usual way"': ' Yes|| No || Unknown}', '"severe"': ' Yes || No || Unknown}', '"numbness paralysis"': ' No || Numbness || Paralysis || Unknown}', '"change behavior"': ' Yes || No || Unknown}'}, 'Heat/Cold exposure:': {'"respond usual way"': ' Yes || No || Unknown}', '"breathing normal"': ' No || Yes || Unknown}', '"full sentence or one word"': ' One/few words || full sentence || not applicable}', '"skin feel"': ' Colder than normal || hotter than normal || normal || unknown}'}, 'INHALATION:': {'"safe out of danger"': ' Yes || No / Unknown}', '"chemicals/fumes  involved"': ' Chemical || Carbon Monoxide || Gas (methane) || Unknown}', '"respond usual way"': ' Unconscious || No || Yes || Unknown}', '"difficulty\tbreathing"': ' Yes\tAND Unconscious || Yes || No || Unknown}'}, 'MOTOR VEHICLE ACCIDENT:': {'"vehicle involved"': ' Multiple\tvehicle || Rollover\t/\tOverturned\t|| Vehicle Bicycle || Vehicle Pedestrian || Vehicle Terrain || Vehicle Motorcycle || Vehicle Vehicle || Vehicle Animal\t/\tPersonal\tMobility\tDevice Pedestrian || Single vehicle (skidded)}', '"trapped"': ' Yes || No || Unknown}', '"thrown"': ' Yes || No || Unknown}', '"everyone able talk"': ' Yes || No || Unknown}', '"obvious"': ' Yes\t/\tUnknown || No}', '"blood"': ' Yes || No}'}, 'POISONING/INGESTION:': {'"What \ttake"': ' Antidepressants|| Acid or Alkali || Cocaine || Narcotics || Over\tthe\tCounter drugs || Alcohol Intoxication || Unknown}', '"weapon"': ' Yes || No}', '"respond usual way"': ' Yes || No || Unknown}', '"attempt"': ' Jumper || Carbon monoxide || Overdose || Stab or Gunshot wound || THREATENING SUICIDE || Laceration / Cut || No || Unknown}', '"blood"': ' Yes || No}'}, 'PSYCHIATRIC / BEHAVIORAL': {'"violent"': ' Yes || No || Unknown}', '"weapon"': ' Yes || No}', '"respond usual way"': ' Yes || No (i.e. not alert) || Unknown}', '"attempt"': ' Jumper || Carbon monoxide || Overdose || Stab or Gunshot wound || THREATENING SUICIDE || Laceration / Cut || No || Unknown}', '"blood"': ' Yes || No / Unknown}'}, 'sick person (specific diagnosis)': {'"difficulty breathing"': ' yes || no || unknown}', '"chest pain"': ' yes || no || unknown}', '"bleeding vomiting blood"': 'Yes || No || Unknown}', '"respond usual way"': 'No || Yes/Unknown}', '"difficulty walking"': 'Yes || Unknown || No}'}, 'stab/gunshot injury(penetrating)': {'"assailant"': 'Yes. One assailant || Yes. More than one assailant || No}', '"resuscitate"': 'Yes || Unconsciousor ARREST || Not Applicable }', '"respond usual way"': 'Yes || No || Unknown}', '"part injured"': ' CENTRAL wounds || PERIPHERAL wounds}', '"morethan one wound"': 'Yes || No || Unknown}'}, 'STROKE/ CVA': {'"respond usual way"': ' YES || NO || UNKNOWN}', '"STROKE"': 'YES||NO||UNKNOWN}', '"what time start"': ' Less than3 hours || More than 3 hours}'}, 'TRAUMATIC INJURIES': {'"respond usual way"': 'Unconscious & breathing (per Case Entry)||No||Yes||Unknown}', '"released"': 'No||Yes||Not Applicable}', '"part of the body"': 'CENTRALbody||PERIPHERALlimbs||Unknown }', '"parts been found"': 'Yes (Amputation CC at end of Question)||No / Unknown||Not Applicable}', '"broken bones"': 'Yes || No|| Unknown}', '"blood"': 'YES||NO||Unknown}'}, 'Unconscious/fainting:': {'"UNCONSCIOUS & NO/UNCERTAIN"': ' No || Yes || Not applicable}', '"respond usual way"': ' Yes || No || Unknown}', '"breathing normal"': ' No || Yes || Unknown}', '"full sentence or one word"': ' One/few words || full sentence || not applicable}', '"history heart problem"': ' Yes || No ||unknown}', '"abdominal"': ' Yes || No || not applicable}', '"more than once"': ' Yes || No || Unknown}'}, 'Unknown:': {'"respond usual way"': ' Yes || No || Unknown || Language Barrier}', '"talk"': ' Yes || No || Unknown}', '"standing, sitting, lying"': ' standing || sitting || lying || unknown}', '"moving"': ' Yes || No/unknown'}}
# print(inc_dic["ABDOMINAL PAIN"]["respond usual way"])


print('inc_dic = ', inc_dic)