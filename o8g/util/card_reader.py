import csv
import os
import re
import sys
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Usage: copy the full table (with column headers) from https://l5r.gamepedia.com/User:Intolerancegaming?profile=no
# Paste it into a spreadsheet and save as csv to l5r.csv. Delimiter is , and text wrapper is ", use ascii (western europe).

# A bit clunky but some IDs had already been assigned and wanted to maintain them.
ids = {
    '1': '9ff46167-1893-45bc-87f6-266f77be7789',
    '2': '8c53e061-b416-4d32-84a1-596c4f3d005a',
    '3': 'f83a2262-031a-4651-b0ec-78fde9cd1f65',
    '4': 'fd38f0c7-45bf-4b85-b572-824fbaa9cba5',
    '5': 'f988df44-9a5e-47d9-bfce-bdfd38c6d9b3',
    '6': '8fc39443-2135-40fb-bece-3889c3dde8a0',
    '7': '0d08602f-ca83-4761-845f-2eb3cae8b74d',
    '8': '40683c9f-b1e9-4055-88bd-ce2a2e846297',
    '9': '98e106b6-7bb4-47c5-9fe7-dd290e3d42df',
    '10': '9cbdfaf2-7559-481d-b5c4-39c2f31a129d',
    '11': '9695237f-1fb2-4716-936e-50fbcf9274b3',
    '12': '99c8a45a-e16a-406b-9029-acf90e0c49bd',
    '13': 'f6388aee-a0b7-48cf-8ac4-e813f1d664df',
    '14': 'cb8186ae-7c61-4be1-b4de-fb43e2b7a44c',
    '15': '82de5aed-145f-4fda-812e-5d1cdf80b0a8',
    '16': '8f0246b6-a8dd-4939-891c-7143c2ac9b53',
    '17': '47d199f8-b178-4bb2-9355-11d16356648b',
    '18': '0549220e-c514-4f95-beac-4471ea24ab10',
    '19': '3a269937-2bc6-4dad-ad7f-1a76b0948e42',
    '20': '90776573-f6a5-45c5-ab3a-204cdd1d1aaf',
    '21': 'a8c4f60e-6c36-4bd7-99da-eef1c3da2aab',
    '22': 'dbcd9eb7-0c13-4906-8d40-339b44a4e6f7',
    '23': '513372c8-9f67-4c26-8f54-7a9fce91b3c1',
    '24': '19c319c6-b2e5-4877-9f6d-b70a64988ea4',
    '25': '35f74bd9-ac4b-4a32-b6d8-667573a006c7',
    '26': '6811de40-d5a3-4cf5-b64f-b31b6c6ea497',
    '27': 'b4950e54-5b1a-4af8-b1a5-c1653b809fda',
    '28': '59fee928-8b62-424e-8024-a31bbd620bd0',
    '29': '15012b1d-41e8-48e5-a3a4-2493a05ec2d1',
    '30': '09d394df-0326-48da-90e2-bf5721a7035a',
    '31': 'b4551ad3-509d-4f07-94c5-8a639d7e1bb0',
    '32': 'c4051433-d797-4fef-81fd-3e7e9c8a2023',
    '33': '0e3f1103-5063-40c9-8f6f-57aec2cdc249',
    '34': 'b9591ff0-c32f-4bd0-9ead-88392c7e5161',
    '35': '59f6b7a8-81fe-4f5c-82ea-9cd0d0cc3eae',
    '36': '8d80f714-c1f8-40ab-9f12-a4d18b82337a',
    '37': 'c7725dcb-9108-4067-9372-ad9e363c0415',
    '38': 'b59201dd-a763-4944-87f4-c21b48a51432',
    '39': '7ddc9756-eaea-4905-b7c7-e9e0b83d1d4a',
    '40': 'f364aac3-9e20-4b59-bebc-19627b0ba91d',
    '41': 'b73d6577-5532-4bd9-9843-0187dd3feff2',
    '42': '291fbfe6-8a12-4f0a-bbb9-78b7de0b4ad9',
    '43': 'e3ea6226-5a5c-4311-a61e-e784169260fb',
    '44': 'da3ab68e-ab00-4dbf-a2f6-111075e3046a',
    '45': 'ead54ee3-d509-458c-bc23-638fded33c64',
    '46': '5de0deef-9cdc-42f7-9cfc-c03bce65bfed',
    '47': 'fea8a1bc-d121-4cfc-9330-6a547f0aad46',
    '48': 'a00790d4-5ae0-41d9-881a-373e14ca40fa',
    '49': 'd59dba2f-3416-4fe7-91a6-f9d3c80cdcd2',
    '50': '64b7f051-9950-408f-accf-001cb8a74a7a',
    '51': 'a9cf0985-a4e6-4874-9a61-c4f480225f23',
    '52': '3935c2f6-c1f3-46b8-a549-16d32f9a99a2',
    '53': '04d91060-4fe5-4191-a6e5-9e423c9f5f8f',
    '54': '5dbe18ad-6493-42fa-8b14-d5cbf933929a',
    '55': '4dae1138-cf99-4880-a600-b8b4d5c6631b',
    '56': 'c7b3b775-e0f2-4786-87aa-59133c0305b6',
    '57': 'd66f08e3-a528-4598-8c96-149155d2abdd',
    '58': '9acf93da-9bb9-473e-b19f-4b873acf8cc2',
    '59': 'a8c52b13-c2fa-4ccf-9d5f-a76436144a41',
    '60': '023b54b4-8fea-4431-a7d4-e28c55a6c03b',
    '61': '6ecdf2e7-bf6d-47c6-85f9-67e3153edd39',
    '62': 'b46be533-47bc-4a02-8de8-e110fed818c3',
    '63': '88ed4ad7-de69-4e41-9a82-1f5fed4d1ded',
    '64': '895e97e4-0f4e-4de7-b478-080f34a37794',
    '65': '6867a986-8eb7-447b-8f09-585d7a416f62',
    '66': '3894796f-3a39-4f7b-aeec-c9df3919b397',
    '67': '7f3b9cca-fa3a-4b17-897f-47da40600657',
    '68': '62140608-93fe-4a57-9e6e-1d686120b7f6',
    '69': '92fb3c5e-a2a0-4a5d-aca8-c867218f7747',
    '70': 'ec52acdd-a2af-49e9-b3e1-2e073bc2a30f',
    '71': '508003aa-e833-4cb5-99a7-15cb9dab508d',
    '72': 'cf5dec4b-7351-4b04-aac2-987df5873bc5',
    '73': 'efd4f883-1a94-4181-8bc6-3bc086b8a3d5',
    '74': '2529a99b-7b5a-4d93-988c-ce8ba4e42a20',
    '75': '47826d27-2a19-4832-ab36-c1fc92b3f948',
    '76': '0f3309d7-375b-44aa-a56a-9230ec696729',
    '77': '9a34b4f5-3cb0-4067-bb49-21a234d4d81b',
    '78': 'c4e39cd4-7536-49df-a00b-883a0a15d7a6',
    '79': '18ff427e-2ce6-4cc6-8e24-09d1df58f756',
    '80': '0c93ed20-599b-4d83-af62-9336e8ab5925',
    '81': 'd42090c2-a6d9-4821-843a-70e0c9e06345',
    '82': '5baae90a-1d1b-4de6-8181-a7dffd7e09e9',
    '83': 'f909e855-0994-4ef8-b350-7152ff4e03f9',
    '84': 'aa0d692d-8767-4ba5-adcb-b7b861821b5b',
    '85': '81f15036-c30a-4424-b7c2-3316bb9a19fa',
    '86': '86ad25a6-ef0a-4216-8bfb-269b5c21efc4',
    '87': 'df86c48d-eba3-4f43-9419-652fea003a89',
    '88': '735ab656-e522-4a8a-86f7-6567ced9b8ad',
    '89': '690729e7-6737-42e9-8b36-d625121842a7',
    '90': '2d9d2a28-d496-4e72-bcb3-6b979376f314',
    '91': '8e0c97c3-ade0-4497-b505-b3e80d4f2aed',
    '92': 'dc87cfc5-f173-44de-9c36-2447d2f0e213',
    '93': '28a84c1a-a155-40f1-a5ed-56c105461423',
    '94': 'bb5532b4-c5b1-449b-85b9-ea88acfb3e57',
    '95': '3fc9117d-1c7c-444e-94e1-19698ce6190a',
    '96': '221a1956-1bac-4aa1-ac9e-4b78ab0bd83c',
    '97': '871af009-a306-4448-acbf-766769633992',
    '98': '30b932e8-8650-44f8-8c9c-3d70a7fed8e7',
    '99': 'cb8008be-33cb-4a82-affe-4cef2ce41981',
    '100': '57fd4f38-7591-4637-a7f6-dd84d31548ef',
    '101': '8fbaa0fa-ef55-4775-a47c-414c3a154dc9',
    '102': 'f8376024-7ca5-4698-a381-e9bb3a18eaae',
    '103': '5c757161-4872-4ae7-9c5e-6d4a75245a77',
    '104': '03f8cf51-5870-419d-bf31-83c1b62dd707',
    '105': 'b5e46d5a-f4e5-4a2a-a754-8d4aa5b7f527',
    '106': '21cf6a90-a206-4854-9b6c-644d83f12522',
    '107': '8a6ae3d6-a34a-4340-ad2d-05304377e8f8',
    '108': 'df365b9f-63cd-4d81-ae02-a69db1d81cea',
    '109': 'f62bb726-4566-4ddf-b160-a6ec4f732557',
    '110': '4c39ba79-1d7e-4b9f-a81a-8b9364307465',
    '111': '080c2783-86c3-4070-b503-501f4acd4433',
    '112': '0a0f5ebc-b682-4a3c-96d2-281758f5f5ad',
    '113': 'a5bc1b90-6094-420c-ad31-a9b3ffb4bdd6',
    '114': 'ec021f72-2e5e-4b7c-88ab-3474658ee98c',
    '115': 'e8d040bb-d41d-4741-9eac-68112deb14ca',
    '116': 'cd33e2bb-2c7b-4c3f-8e0d-87bfc7c48bc1',
    '117': '26564d02-8f88-4ba2-99b9-6c5f9d499768',
    '118': '8bec26c1-94c8-4a30-8138-28f7465f00d2',
    '119': '7742aa81-4781-4846-a1d1-9c4446f6373f',
    '120': 'a74c2bdb-45c4-40ac-b5df-b92cf92503df',
    '121': '50b1ae8a-6257-4991-bb62-00b979c7c0f0',
    '122': '67b18356-65a2-4a04-8d15-4e5425ab4160',
    '123': '9dc58761-e779-4b88-9405-eabf6edcf1ea',
    '124': '7750490a-5dfb-4960-bd4b-2b800174a5ef',
    '125': '708ff8aa-3b55-4a59-a13f-a9b2b0b63ae2',
    '126': 'ecab8b91-acd6-46f0-8f9b-991bfe1a599e',
    '127': '21bb93d6-537d-4084-bda1-e3647789fee8',
    '128': '8dd56bff-5761-4075-9dde-2dba1452e6f6',
    '129': 'eac25eba-25ae-4d38-b1f0-01cfe5cc35df',
    '130': '8b4ece45-02c7-42a2-978b-d8ea103890d5',
    '131': 'c6a61750-9202-4c6d-b30b-ce843f1316a6',
    '132': '4754fed3-44b5-4d6f-bac9-e8dce9028712',
    '133': '56ba414a-40b0-4be2-9a40-417541dbf7fe',
    '134': '5df9e7d3-676f-42dd-880c-68fa8e11dbcd',
    '135': '556841cb-d05e-4d5c-8dc0-4706f88e044c',
    '136': '9f06d1b0-4a4c-4b76-a44e-2bef3b37a785',
    '137': '9cd1be8a-c729-45d6-9b9f-32bf38058a0c',
    '138': '6b2b7025-af74-474a-8dee-61efb544122b',
    '139': 'ad350407-e999-4da0-b136-dd046375e07a',
    '140': '81ee4125-ccbb-4ee2-b156-bd479181dbe0',
    '141': '2abecb53-9c4c-45d7-8a26-787af66511fd',
    '142': '3cab40e6-8964-4aa7-aead-378bbdd87ed1',
    '143': '2536d187-8579-4c38-bc95-460444803797',
    '144': '06c75060-149d-4f18-8473-8358dc9f751a',
    '145': '61870bd9-a875-4e63-b261-c271a8097d48',
    '146': '8e1d1326-c2cc-48db-ad41-8e26ce78a4bb',
    '147': '916f4fab-1e57-444e-bdbe-8cd7eeb956c8',
    '148': '27a2aea7-18e8-403c-88cb-74d240b772e9',
    '149': 'bf7ed11c-05e4-4b12-aa6e-54e737a5eb04',
    '150': 'f1efd236-4b40-4726-8d0b-26777af79d97',
    '151': '0c57ad14-3794-4d09-badf-596134dab781',
    '152': '6c6f9607-f925-4523-9b81-c4e589f5b8bb',
    '153': '847acaeb-0176-4dae-99d6-e91a1a96e614',
    '154': '5aaaabac-df50-429d-8013-2607ec17c1c9',
    '155': '798c3705-f26f-4040-bd41-58347c28c8c3',
    '156': '5311700e-ab90-4ccd-a63b-c4ee65001d33',
    '157': '82777c2f-1a7e-4bf9-8ed7-11c06aa6e97d',
    '158': '6aa2734d-5513-4ce5-8962-2146ee87a6d7',
    '159': '22311657-8eca-4253-b757-b1bf48665cea',
    '160': '0036d752-5951-422d-b05e-e3cde23bc26a',
    '161': 'd7d060b0-d3b8-48e0-8eff-d2f40ac62eff',
    '162': '0519ea31-2708-4bc3-a913-8b955b3971ab',
    '163': '0506f09d-431a-45ee-bc2a-c60f4b28cef3',
    '164': '6533e650-b569-4530-8bf6-262396135b1b',
    '165': '0d320b35-9c12-4608-85f3-067abc04ba88',
    '166': 'a1bce639-2b1e-49b4-a197-1e10c3ba843f',
    '167': '7bbc1cad-9a17-4730-bab3-b500f9a7f97b',
    '168': '24733b42-986b-4471-b704-18af9903b3b1',
    '169': 'bf3be207-24ae-4276-92c0-16ce7cb83840',
    '170': 'f69ef98f-8e95-496d-bae2-9eb8b1870bbd',
    '171': '42aff476-2841-41cb-b3fe-d29b33af41c8',
    '172': 'a7f0643d-2875-4f23-843a-40bfeec07227',
    '173': 'ed79352d-950a-4904-8887-c8b893fb9659',
    '174': 'b1dcf0f9-2ee4-4274-99db-21d749ffa435',
    '175': 'd89d3732-716a-413f-999b-2b39535ccddf',
    '176': 'f07a6ceb-e5ca-4ab8-b193-120e4f3507e1',
    '177': 'bc87d1b4-28ea-4874-9d20-99e08efe753c',
    '178': 'd8e881bd-66c8-4103-9c0e-4953d028044b',
    '179': 'f71abfbd-985e-4f1b-b61f-773a02f82486',
    '180': 'e3768195-9e62-4468-8ef4-5349c2a4f1ad',
    '181': '3f288e4d-8003-4f8e-94ab-318110500035',
    '182': '4997589a-6b02-45e2-a6ba-6ee8084af295',
    '183': '2e197bbc-d6bc-441b-92c4-0583848d30bc',
    '184': 'cd99242a-29bb-49dd-82d8-cec775afd764',
    '185': '6c18d7c6-03fb-4717-93f3-e44314efae56',
    '186': 'e71194e8-30ae-4e8e-a053-d6d7ce0cb149',
    '187': 'ed546e3d-c954-4354-94fe-5bce936b649e',
    '188': 'f2ca9035-de1c-4539-8cb8-cc504e47156c',
    '189': 'e0949fb5-72cc-47da-bfef-979d967aff28',
    '190': 'c5538aa2-657a-43b1-9224-76f10dd6d4e4',
    '191': '5e815eda-983a-4afe-ba7d-5e6c7e421a6d',
    '192': 'b288d363-9dcf-4853-9b83-65c20b53863c',
    '193': '9131e723-ebd2-4154-b7a1-d2ab8731950d',
    '194': '98db54e5-2bc2-4bcf-bd55-a49b3783b387',
    '195': '2add7f54-6d9e-44b3-b0aa-df45e4106382',
    '196': '04b588fd-bb81-4222-88d4-44f0c1ee35a8',
    '197': '5cf714bf-5dd7-44bb-906c-734182886b9d',
    '198': '3a4a2547-142c-4394-81fc-314fd3a14236',
    '199': 'a18a5893-9931-4cb5-a1e9-49c6e8a9fcb0',
    '200': '0d11eb2f-2f27-4bf8-bc25-752e367e045a',
    '201': '0f8ce9b0-be45-42a8-a310-bab3bc4660d7',
    '202': '6d8d67f8-38ea-4db2-a5d5-2f54b9493f33',
    '203': '3b85a2ef-1f9c-4c3f-bc17-f427effc1a14',
    '204': '84ed44dc-0324-4f88-90ff-1d4b0679be8d',
    '205': '04ebdaa2-b46a-49c7-a0ba-1855504b4a12',
    '206': 'b814b1f3-f7e9-462a-99ed-448937dfc1a8',
    '207': '4943895d-ab44-4571-ae49-2f51781469ad',
    '208': '485cc3e7-1fd1-4ba1-8a6d-3a2c476b9993',
    '209': '95b10d7c-092b-414d-af65-bc351d1ce8ab',
    '210': 'b618c2aa-9687-491a-aa7d-7e284264583c',
    '211': '613a8a9f-4b3f-4ea4-90ed-3d7423d8423a',
}

if len(ids.keys()) != 211:
  sys.exit('Invalid number of uuid keys')
for key in ids.keys():
  if int(key) < 1 or int(key) > 211:
    sys.exit('Invalid card number in uuid keys')

icon_regex = re.compile(r'\[\w+\]', re.IGNORECASE)

if (len(sys.argv) != 2):
  sys.exit('Usage: {} <l5r.csv>'.format(os.path.basename(sys.argv[0])))

set = Element('set')
cards = SubElement(set, 'cards')

with open(sys.argv[1], 'rb') as f:
  reader = csv.DictReader(f, delimiter=',', quotechar='"')
  for row in sorted(reader, key=lambda r: r['ID'].strip() and int(r['ID']) or 9999):
    if row['ID'].strip() != '':
      attr = {'id': row['ID'].strip() in ids and ids[row['ID'].strip()] or '', 'name': row['Name'].strip()}
      if row['Deck'].strip():
        attr['size'] = row['Deck'].strip().lower()
      card = SubElement(cards, 'card', attr)
      if row['Clan'].strip():
        SubElement(card, 'property', {'name': 'Clan', 'value': row['Clan'].strip().capitalize()})
      else:
        SubElement(card, 'property', {'name': 'Clan', 'value': 'Neutral'})

      SubElement(card, 'property', {'name': 'Type', 'value': row['Type'].strip().capitalize()})

      if row['Unique'].strip() == '1':
        SubElement(card, 'property', {'name': 'Unique', 'value': 'Unique'})

      SubElement(card, 'property', {'name': 'Traits', 'value': row['Traits'].strip()})
      SubElement(card, 'property', {'name': 'Text', 'value': re.sub(icon_regex, lambda m: m.group().title(), row['Text'].strip())})

      if row['Cost'].strip() != '':
        SubElement(card, 'property', {'name': 'Cost', 'value': row['Cost'].strip()})

      if row['Military'].strip() != '':
        SubElement(card, 'property', {'name': row['Type'].strip().capitalize() == 'Attachment' and 'Bonus Military Skill' or 'Military Skill', 'value': row['Military'].strip()})
      elif row['Type'].strip().capitalize() == 'Character':
        SubElement(card, 'property', {'name': 'Military Skill', 'value': '-'})

      if row['Political'].strip() != '':
        SubElement(card, 'property', {'name': row['Type'].strip().capitalize() == 'Attachment' and 'Bonus Political Skill' or 'Political Skill', 'value': row['Political'].strip()})
      elif row['Type'].strip().capitalize() == 'Character':
        SubElement(card, 'property', {'name': 'Political Skill', 'value': '-'})

      if row['Glory'].strip() != '':
        SubElement(card, 'property', {'name': 'Glory', 'value': row['Glory'].strip()})

      if row['Strength'].strip() != '':
        SubElement(card, 'property', {'name': 'Bonus Strength', 'value': row['Strength'].strip()})
      
      if row['Honor'].strip() != '':
        SubElement(card, 'property', {'name': 'Starting Honor', 'value': row['Honor'].strip()})
      
      if row['Fate'].strip() != '':
        SubElement(card, 'property', {'name': 'Fate Value', 'value': row['Fate'].strip()})
      
      if row['Influence'].strip() != '':
        SubElement(card, 'property', {'name': 'Influence Value', 'value': row['Influence'].strip()})

      if row['Ring'].strip() != '':
        SubElement(card, 'property', {'name': 'Ring', 'value': row['Ring'].strip().capitalize()})

      SubElement(card, 'property', {'name': 'Card Number', 'value': row['ID'].strip()})

    
reparsed = minidom.parseString(tostring(set))
print reparsed.toprettyxml(indent="  ")
