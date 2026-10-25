"""500 manual contextual Navi/mail/folder/NPC drafts; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
    "69EF48": ["ac4c289be330a8d62ef2e5a5176e02e977c6d0e9d511ade4403e98c5213daef9",15,"translations/batch500_045_navi_mail_npcs_69EF48_draft_ko.json"],
    "6A26C8": ["66543a0c21f049f8b733dc9db4aed07500cfcea33a57f45eda70e046d746e1c7",5,"translations/batch500_045_navi_mail_npcs_6A26C8_draft_ko.json"],
    "6A383C": ["f433a81be645bb7377ad02cc91118664ed4b561aa18dd080bf398da54f7a13e6",6,"translations/batch500_045_navi_mail_npcs_6A383C_draft_ko.json"],
    "6A3D48": ["405c9ab74526a0691e5bb344d25f550ee8b6bfebb6b52d6eb924e1344e3f65b1",4,"translations/batch500_045_navi_mail_npcs_6A3D48_draft_ko.json"],
    "6A4BF0": ["321936b4c0001933bb2e6364edf86d35d2a7d6cf6fe61277228a9d361f1403b7",5,"translations/batch500_045_navi_mail_npcs_6A4BF0_draft_ko.json"],
    "6A5578": ["429ccdac20978e8396c6bc8d2f3694eee5b2d4544b2c07faae47fce93e95552f",7,"translations/batch500_045_navi_mail_npcs_6A5578_draft_ko.json"],
    "6A570C": ["84c728f6ba6ed25a8d8f4c67cfc9e298018438dff17777cbfdd70204d357cd91",6,"translations/batch500_045_navi_mail_npcs_6A570C_draft_ko.json"],
    "6A8A08": ["3ac659675349230d2bea55e1af6e465220da5425a44bf23a42f60d60bf4f9915",6,"translations/batch500_045_navi_mail_npcs_6A8A08_draft_ko.json"],
    "6A907C": ["d51ed15571aafcffde5387f768862133673f6509442e449d78054e72bb80c68f",4,"translations/batch500_045_navi_mail_npcs_6A907C_draft_ko.json"],
    "6AA1A0": ["2aa035643bdbf5dbda493c248c62b119a503a5a2ffca6e75a7fc59f06d9da841",2,"translations/batch500_045_navi_mail_npcs_6AA1A0_draft_ko.json"],
    "6AA6A0": ["0af7fef1273890d5743fca2ca7a51884af1752ae8f0bf4b7532af9b181fac7a8",3,"translations/batch500_045_navi_mail_npcs_6AA6A0_draft_ko.json"],
    "6AAEB0": ["7d8c18da2b2dfab697cbc7e9971045204c8af25bc8677b10667c912732b6f1df",15,"translations/batch500_045_navi_mail_npcs_6AAEB0_draft_ko.json"],
    "6AB458": ["65c7725d32418a980e837b0e33a53b672e39da034486fc6bd32c02d793ce6495",9,"translations/batch500_045_navi_mail_npcs_6AB458_draft_ko.json"],
    "6AE758": ["910f9da3208031c1496d9ff920c23142ebadc7dc049a7d752f77ef5b8f666a09",5,"translations/batch500_045_navi_mail_npcs_6AE758_draft_ko.json"],
    "6AED8C": ["84f2250b3b85d4548c818527ae6eb18325a55216eaa2c9569ba92805bbd435e2",6,"translations/batch500_045_navi_mail_npcs_6AED8C_draft_ko.json"],
    "6B5FB0": ["8cc725594bfb94f71b598271a6168005d1cad904376758d4f53e818abf7ca846",4,"translations/batch500_045_navi_mail_npcs_6B5FB0_draft_ko.json"],
    "6B60F0": ["41bd6aa19b53d24e68bf052b082d43a34f634cd6b40e3489584ec376c40c4703",1,"translations/batch500_045_navi_mail_npcs_6B60F0_draft_ko.json"],
    "6B69A0": ["823d71e7901e9226aad5de3617d43d2c6c4700557500a7487d8100a7adb5acaf",10,"translations/batch500_045_navi_mail_npcs_6B69A0_draft_ko.json"],
    "6BA2BC": ["377f32d6d6132c914f443017af24df7bdbc06fc1387ac1d0eefff63b85b002bf",7,"translations/batch500_045_navi_mail_npcs_6BA2BC_draft_ko.json"],
    "6BA910": ["4662f7d407cb1666754be273cb95dd25c6e137ada5fe7e6f95c530d1a42723fd",5,"translations/batch500_045_navi_mail_npcs_6BA910_draft_ko.json"],
    "6BBAF8": ["7d284efbaf15b46d413a95f39aed78b4129c8f05a622eb5150624063fe54d150",6,"translations/batch500_045_navi_mail_npcs_6BBAF8_draft_ko.json"],
    "6BC034": ["ad806a319f0cf58f5bc6a97fd08a7c300faa5955b7d978811febab84b8f8b47f",3,"translations/batch500_045_navi_mail_npcs_6BC034_draft_ko.json"],
    "6BC0C8": ["409ee8b81f35ed98f91bc22b7fc15f4fbd071a7126252dc6a6cea24a6f2866e3",12,"translations/batch500_045_navi_mail_npcs_6BC0C8_draft_ko.json"],
    "6BC2F8": ["ec6301c9d562d0332d40da54523118420e81b019f67c50df6435716778b2292b",1,"translations/batch500_045_navi_mail_npcs_6BC2F8_draft_ko.json"],
    "6BC74C": ["d4e981e6cc165aaff571db69a66374296b29ce6883da982d0ba2aa1d3beafbab",15,"translations/batch500_045_navi_mail_npcs_6BC74C_draft_ko.json"],
    "6BCCD0": ["ad22f62a94849cf9a5bef29eeb7d91f4b77397e464e82942cc6c60471ff85137",11,"translations/batch500_045_navi_mail_npcs_6BCCD0_draft_ko.json"],
    "6BCEB4": ["7c17a681d8ced94574c5a99b823788d22df2a2fab7c8e55c3c574c925cd6ff61",6,"translations/batch500_045_navi_mail_npcs_6BCEB4_draft_ko.json"],
    "6BFF50": ["4a7ab67236b51e62742f8f29be6b58ee0e5372e0e5b29fbd98213a098f86fd64",7,"translations/batch500_045_navi_mail_npcs_6BFF50_draft_ko.json"],
    "6C04FC": ["d28dba172438feab212ba1403fe006868e0412a682a0dd6c3ee7d7c6769d8ffe",5,"translations/batch500_045_navi_mail_npcs_6C04FC_draft_ko.json"],
    "6C167C": ["f06c4f137e75347210e9414256e52004a1d8a8a65a0f2abd353c19b2a5aa6b8b",4,"translations/batch500_045_navi_mail_npcs_6C167C_draft_ko.json"],
    "6C1B84": ["3bb54e6ccdd2ae83ac4214883899663945d5afd9db683dac84d4aad1ff4e2d6c",3,"translations/batch500_045_navi_mail_npcs_6C1B84_draft_ko.json"],
    "6C2368": ["7072185f7bca81af930141c4633a4ae362b935395dfb3844e60f939909d398b6",18,"translations/batch500_045_navi_mail_npcs_6C2368_draft_ko.json"],
    "6C2D3C": ["49fac6e4c17fcf1706c5ec32b3f967f3acfa6d7131aca0dea9fd6a890ee82f1e",6,"translations/batch500_045_navi_mail_npcs_6C2D3C_draft_ko.json"],
    "6C5994": ["4226d314510a7a1d45627b5c779741025acf77cba0a37709ab26af5fa125e0eb",6,"translations/batch500_045_navi_mail_npcs_6C5994_draft_ko.json"],
    "6C5F28": ["de41d433b1159c06de3d32ce0e7647c0db1767f22c0e12c49d602c789277a959",3,"translations/batch500_045_navi_mail_npcs_6C5F28_draft_ko.json"],
    "6C7084": ["8666b2ec53b82a4363f2609adee44e3a221675ed035bd199750044079a739619",5,"translations/batch500_045_navi_mail_npcs_6C7084_draft_ko.json"],
    "6C7594": ["b0bdd94b4a6f866b879bad04322577a9d6cb665ee8cd034acfad245aaf36c5cc",3,"translations/batch500_045_navi_mail_npcs_6C7594_draft_ko.json"],
    "6D1068": ["f1a00ff11381d3d5cef81e897a8ee564fc99b36c4faa3e3ac0b92ceda965decc",3,"translations/batch500_045_navi_mail_npcs_6D1068_draft_ko.json"],
    "6D2180": ["1703af1a97c53fc28dfeeb595168d027dd758cbc4c96c479f52e757ea9997dd7",5,"translations/batch500_045_navi_mail_npcs_6D2180_draft_ko.json"],
    "6DD63C": ["9fb5da0978dfd24ba044bb68a7e748768fb51d6f984cb6600aa17b275c5b4740",22,"translations/batch500_045_navi_mail_npcs_6DD63C_draft_ko.json"],
    "6DD718": ["f41b511165f5686525b26360e9d89e1500077c27e5234965e4bcf5365d26cd56",16,"translations/batch500_045_navi_mail_npcs_6DD718_draft_ko.json"],
    "6DD798": ["6363e5b2278354fa8207bf069ed9fc18fd4fa0e4303cb3b32c1e04d76abf25b5",10,"translations/batch500_045_navi_mail_npcs_6DD798_draft_ko.json"],
    "6DD804": ["dcc6cf49dc5e18ae6289c65b785a3a9c981864c2458cfdd7d4516c547fd42135",10,"translations/batch500_045_navi_mail_npcs_6DD804_draft_ko.json"],
    "6DD91C": ["3ee4d5175b121b316044495482897a905466e9978b274a8b289d3929a979ad92",32,"translations/batch500_045_navi_mail_npcs_6DD91C_draft_ko.json"],
    "6DE2C8": ["0e900e5e87e0b52bbdc30d72365b87a73baab2bac60514a60946f933f05df5b6",15,"translations/batch500_045_navi_mail_npcs_6DE2C8_draft_ko.json"],
    "6E2B9C": ["a5d2b80bdd1526dd91693b918031c100ea94ac4954c5d811e7f80ce4af4eb635",14,"translations/batch500_045_navi_mail_npcs_6E2B9C_draft_ko.json"],
    "79C240": ["15b2882dc2e1185f81cda0f0f541cf48c57ddce325d0ec3d93ef1e810503d654",3,"translations/batch500_045_navi_mail_npcs_79C240_draft_ko.json"],
    "79C518": ["2dcf15ab278e5b02593b2526d5f15dcdb8f73e52bf45b0320cc3bfac11e3d952",2,"translations/batch500_045_navi_mail_npcs_79C518_draft_ko.json"],
    "79C554": ["37adcdb3e1f6739f9a2343787bafa4376c09ea9530e9fc6cf60be6c977d4fb29",2,"translations/batch500_045_navi_mail_npcs_79C554_draft_ko.json"],
    "79C590": ["cfb4a850b195045c46a726fd2ac2ba034f28f57888c82161f388e25512f4000e",2,"translations/batch500_045_navi_mail_npcs_79C590_draft_ko.json"],
    "79C5CC": ["666e54b6bd8c8afa03f63f42e108a960aa6155e41147a76c31ee48c3386ae7b9",2,"translations/batch500_045_navi_mail_npcs_79C5CC_draft_ko.json"],
    "79CB64": ["e552ce2821923e7dfb6540593e10684632ae993805bc59499815c722688f508b",3,"translations/batch500_045_navi_mail_npcs_79CB64_draft_ko.json"],
    "79CBCC": ["c465ea7ca83c96171b7b747b45bde8a4e28386a9e2d6ae0664bb2291d9e7786e",1,"translations/batch500_045_navi_mail_npcs_79CBCC_draft_ko.json"],
    "79CC08": ["9236c7d4841edba34a88ffedf8e0135926e78ee5d21b1a8f3448b6bdc93bc2c7",2,"translations/batch500_045_navi_mail_npcs_79CC08_draft_ko.json"],
    "79CC44": ["6dd51d765fb03d8dcdad3a2f12662123529a29c7c3e736b92d6659efdfc4c9b6",1,"translations/batch500_045_navi_mail_npcs_79CC44_draft_ko.json"],
    "79CCB0": ["024eef595100aaa3926734e24dc68ea74b4551fefbf002932215bc161da5d4e4",20,"translations/batch500_045_navi_mail_npcs_79CCB0_draft_ko.json"],
    "7A7C04": ["68264437baee0484f4baa475e8b05c42902d138916db5c890342c6efaad02f43",4,"translations/batch500_045_navi_mail_npcs_7A7C04_draft_ko.json"],
    "7A7CF8": ["355cd69cb2bbf2e89fce6caaacbd9e2931402ffe04d873a9246fca1ee6fdc3a6",6,"translations/batch500_045_navi_mail_npcs_7A7CF8_draft_ko.json"],
    "7A7EF8": ["1b2fb2d28f8351e1897f91af17434730829419fe9a902938a255e928d2f7d992",4,"translations/batch500_045_navi_mail_npcs_7A7EF8_draft_ko.json"],
    "7A8864": ["942fd28924f553f29e3dc650e752d4be47d45dbeb7a89ddc27054d3cb95c3f2e",4,"translations/batch500_045_navi_mail_npcs_7A8864_draft_ko.json"],
    "7A8AE0": ["c437ff94641f8b741e5f40ba47c6b95fd08b1a1a6228f53e39f62c63fa5c2d19",3,"translations/batch500_045_navi_mail_npcs_7A8AE0_draft_ko.json"],
    "7A8E20": ["ff875c07e23c2637ca7366d16599b78e31d09fc42e3c85b95b7bc432960ebcad",3,"translations/batch500_045_navi_mail_npcs_7A8E20_draft_ko.json"],
    "7A99C0": ["7bb54684fbe61fd8ad2a974b11c26e93e3e440496280603a678d8956a80fedbf",5,"translations/batch500_045_navi_mail_npcs_7A99C0_draft_ko.json"],
    "7A9BA0": ["ae3518e44f653fa7f5690b8f8f5edeee9c64392683bfd4c8a4eff28521a152a3",8,"translations/batch500_045_navi_mail_npcs_7A9BA0_draft_ko.json"],
    "7A9CAC": ["7bcfa9470eb0db68202b79956aaa882c612d285d8b815c6f9b915e67ca39e576",8,"translations/batch500_045_navi_mail_npcs_7A9CAC_draft_ko.json"],
    "7A9DA8": ["0eb07e3cb6833ce7c3a62caa13c1b35b48451ecc3f6978f9e4bbef6d89d57abd",3,"translations/batch500_045_navi_mail_npcs_7A9DA8_draft_ko.json"],
    "7A9E44": ["83d5478c83de85dae632e915448eadfa94b43f908c8d2e3ec37e28999569b2a9",2,"translations/batch500_045_navi_mail_npcs_7A9E44_draft_ko.json"],
    "7AAB30": ["0562de32ba2cbf5d68e5b2f91cbb7abb566697457c57d6486bf39e0869686470",1,"translations/batch500_045_navi_mail_npcs_7AAB30_draft_ko.json"],
    "7AABB0": ["64ab3b2a850dbd5c6e2f4ea926190c9bd51e063e89007cf1ffc32714d8a3be13",7,"translations/batch500_045_navi_mail_npcs_7AABB0_draft_ko.json"],
    "7AACC0": ["9cdc22922d23f0105210b6b95c1fabc610695b4964f20a72bd4eb81d85d0f3db",3,"translations/batch500_045_navi_mail_npcs_7AACC0_draft_ko.json"],
    "7AAD84": ["36820e386b7becc62e5fd94753dd500fad0beaeb72263d70d451ef31aea4c2bb",12,"translations/batch500_045_navi_mail_npcs_7AAD84_draft_ko.json"],
    "7AAEF0": ["bf5609f5c5ea3ddf26b86f1f09c6e2aea80be0a820dfb11660b3ee497c14d8f3",3,"translations/batch500_045_navi_mail_npcs_7AAEF0_draft_ko.json"],
    "7AB420": ["3ddba2d84bd6d650988348648cbdebbc2f19fd53792008c2836e7da0041024e2",2,"translations/batch500_045_navi_mail_npcs_7AB420_draft_ko.json"],
    "7AD8D0": ["feaceefad3e153ef65a611de6e8fc62554853d375e252ee27688b479a0576501",4,"translations/batch500_045_navi_mail_npcs_7AD8D0_draft_ko.json"],
    "7AD978": ["8206e9ba1572a3050f0d91a1b740a44314c26a000cd5fa6a9083dfb4e5c952d4",5,"translations/batch500_045_navi_mail_npcs_7AD978_draft_ko.json"],
    "7ADA60": ["ad8a83fa2d3544dae11a7b8434970227b274c54cad3b4ab473f5d2c95f5ea210",9,"translations/batch500_045_navi_mail_npcs_7ADA60_draft_ko.json"]
}
DRAFT={
  "69EF48": {
    "1:0": "이번에는 졌지만\n승부에는 운도 따르는 법,",
    "1:1": "큰 나무처럼 든든히\n버티고 있으면",
    "1:2": "승리는 저절로\n보이게 된다...",
    "2:0": "해냈구나...",
    "2:1": "이 승리 또한\n대지의 은혜...",
    "2:2": "위대한 대지에\n감사하도록 하자",
    "10:0": ",\n참가 등록이 안 되어 있다",
    "20:0": "전력을 다해 맞서자\n",
    "20:1": "...",
    "21:0": "전력을 다해 맞서자\n",
    "21:1": "...",
    "22:0": "전력을 다해 맞서자\n",
    "22:1": "...",
    "23:0": "전력을 다해 맞서자\n",
    "23:1": "..."
  },
  "6A26C8": {
    "1:0": "안타깝구나...",
    "1:1": "너는\n너무 착하다...",
    "2:0": "해냈구나...\n",
    "2:2": "이 승리를,\n대지에 바치자!",
    "3:0": "아직 마무리가\n빈틈이 많구나..."
  },
  "6A383C": {
    "1:0": "안녕!\n처음 만나네!!",
    "1:1": "나는 스타맨,\n사이좋게 지내자!",
    "2:0": "반짝!",
    "2:1": "또 함께\n해 줄 거야?",
    "2:2": "역시 내가 없으면\n반짝임이\n부족하지?",
    "2:3": "잘 부탁해!"
  },
  "6A3D48": {
    "1:0": "슈타앙!!",
    "1:1": "혜성처럼\n스타맨,\n지금 도착!",
    "2:0": "하아~아,",
    "2:1": "오늘 배틀의 빛은\n6등성 정도로\n희미했네..."
  },
  "6A4BF0": {
    "1:0": "플러그인!\n스타맨.EXE,\n트랜스미션!!",
    "2:0": "오늘은 별로\n내키지 않네...",
    "2:1": "플러그인,\n그만두면 안 될까?",
    "2:2": "라고 해도\n하겠지...",
    "3:0": "오늘은 좋은 날이\n될 것 같은 느낌이야!"
  },
  "6A5578": {
    "1:0": "아아, 별똥별이여!!\n우리에게 승리를\n내려 주소서~",
    "2:0": "해냈어, 우승이야!!\n별똥별에게 소원이\n전해졌나 봐!",
    "10:0": ",\n참가 등록이 안 됐어!",
    "20:0": "왠지 두근거리네!\n힘내자!!",
    "21:0": "왠지 두근거리네!\n힘내자!!",
    "22:0": "왠지 두근거리네!\n힘내자!!",
    "23:0": "왠지 두근거리네!\n힘내자!!"
  },
  "6A570C": {
    "1:0": "맞다! 이제 곧,",
    "3:0": "일정의 시간이었지!",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없어",
    "11:2": " 부터\n",
    "12:0": "야!"
  },
  "6A8A08": {
    "1:0": "주말에 열리는\n토너먼트,",
    "1:1": "우승할 수 있도록\n별똥별에게\n빌어 두자!",
    "2:0": "오늘은 토너먼트가\n열리는 날이네!",
    "2:1": "전부 승리의 별로\n채우고 싶네!",
    "3:0": "뭔가 재미있어 보이는\n아이템이 있어!",
    "3:1": "키 아이템을\n살펴보자!"
  },
  "6A907C": {
    "1:0": "뭐야, 패배의 검은 별이네\n......",
    "2:0": "역시 패배의 검은 별보다는\n승리의 하얀 별이\n좋지!",
    "3:0": "무승부...",
    "3:1": "검은 별도\n하얀 별도 아니네...\n회색 별?"
  },
  "6AA1A0": {
    "1:0": "소인은 섀도맨\n잘 부탁드리겠소\n...",
    "2:0": "소인이 나설 차례인가\n..."
  },
  "6AA6A0": {
    "1:0": "훗, 요즘의\n바이러스들도\n별것 아니구려",
    "2:0": "그 정도 상대에게\n뒤처지다니...\n이 무슨 불찰이오!!",
    "2:1": "소인도 수련이\n부족한 모양이오..."
  },
  "6AAEB0": {
    "1:1": ",\n메일이 왔소...",
    "2:1": ",\n메일이 왔소...",
    "3:1": ",\n메일이 왔소...",
    "4:1": "메일이 왔소...",
    "5:1": "메일이 왔소...",
    "6:1": "메일이 왔소...",
    "7:1": "메일이 왔소...",
    "10:1": ",\n암살 의뢰가\n도착했소...",
    "20:1": "메일이 왔소...",
    "21:1": "메일이 왔소...",
    "22:1": "메일이 왔소...",
    "23:1": "메일이 왔소...",
    "24:1": "메일이 왔소...",
    "25:1": "메일이 왔소...",
    "26:1": "메일이 왔소..."
  },
  "6AB458": {
    "1:0": "많은 이들 앞에서\n닌자가 실수를 하다니,\n이 무슨 굴욕이오!!",
    "1:1": "이대로 물러설 수는\n없소...",
    "2:0": "소인의 인술을,\n똑똑히 보았소...",
    "2:1": "린, 효, 토,\n샤, 카이, 진,\n레츠, 자이, 젠!!",
    "10:0": ",\n참가 등록이 안 되어 있소",
    "20:0": ",\n자, 출진이오",
    "21:0": ",\n자, 출진이오",
    "22:0": ",\n자, 출진이오",
    "23:0": ",\n자, 출진이오"
  },
  "6AE758": {
    "1:0": ",\n수련은 하지\n않아도 되겠소...",
    "1:1": "주말에\n토너먼트가\n열리지 않소?",
    "2:0": "오늘 토너먼트에서,\n소인의 닌자 기술을\n마음껏 보여 주겠소",
    "3:0": "...뭔가\n재미있어 보이는 아이템이\n있는 모양이구려...",
    "3:1": "키 아이템을\n살펴보지 않겠소?"
  },
  "6AED8C": {
    "1:0": "인술의 빛이\n흐려졌구려...",
    "1:1": "심두멸각!!",
    "1:2": "린, 효, 토,\n샤, 카이, 진,\n레츠, 자이, 젠!!",
    "2:0": "소인의 인술 앞을\n가로막는 자를\n기다리는 것은...",
    "2:1": "오직 삭제뿐!!",
    "3:0": "무승부로는,\n소인은\n만족하지 못하오..."
  },
  "6B5FB0": {
    "1:0": "나이트맨, 지금\n돌아왔소",
    "1:1": ",\n훌륭한 오퍼레이션\n이었소",
    "2:0": "크윽! 나이트맨,\n일생일대의 불찰이오!!",
    "2:1": "다음 기회에는\n반드시,\n명예를 되찾겠소"
  },
  "6B60F0": {
    "1:0": "플러그인!\n나이트맨.EXE,\n트랜스미션!!"
  },
  "6B69A0": {
    "1:0": "내가 이런 실수를...\n면목이 없소",
    "1:1": "이 나이트맨,\n다음에는 배수의 진으로\n싸움에 임하겠소!",
    "2:0": "!\n해냈소!!",
    "2:1": "승리의 함성이오!\n승리의 함성을 지릅시다",
    "2:2": "에이, 에이, 오!!\n에이, 에이, 오!!\n에이, 에이, 오!!",
    "10:0": ",\n참가 등록이 안 되어 있소",
    "20:0": "싸울 때가\n왔소!!\n자, 갑시다!",
    "21:0": "싸울 때가\n왔소!!\n자, 갑시다!",
    "22:0": "싸울 때가\n왔소!!\n자, 갑시다!",
    "23:0": "싸울 때가\n왔소!!\n자, 갑시다!"
  },
  "6BA2BC": {
    "1:0": "우오오오옷!!",
    "1:1": "!\n특훈이오!!",
    "1:2": "토너먼트가\n열리는 주말이\n다가오고 있소!!",
    "2:0": "오늘 토너먼트에서,\n이 나이트맨,\n기사의 긍지를 걸고",
    "2:1": "전력을 다해\n싸우겠소!!",
    "3:0": ",\n뭔가 재미있어 보이는\n아이템이 있소!",
    "3:1": "키 아이템을\n살펴봅시다!"
  },
  "6BA910": {
    "1:0": "전법이 단조로워지고\n있는 것 같다는\n생각이 드는구려...",
    "1:1": "칩을 사용하는 방식에\n조금 더 변화를\n주면 어떻겠소?",
    "2:0": "의 경우,\n제법 뛰어난\n책략가이시구려!",
    "2:1": "하지만 계략에\n빠져들지 않도록,\n주의하시오!",
    "3:0": "다음에는 반드시\n승부를 가르겠소!!"
  },
  "6BBAF8": {
    "1:0": "난 네이팜맨!!",
    "1:1": "우선 뭘\n박살 내 볼까?",
    "1:2": "난 빨리\n쏴 버리고 싶어서\n몸이 근질거린다고!!",
    "2:0": "야,\n날 내버려 두고\n뭘 하고 있었던 거야?",
    "2:1": "상당히,\n짜증이\n쌓였다고",
    "2:2": "빨리 싸우게 해 줘!"
  },
  "6BC034": {
    "1:0": ",\n마음껏 쏘게 해 줘!!\n아직 한참 부족하다고!",
    "2:0": "정말이지,\n보통 그런 상황에선\n칩 공격을 하잖아?",
    "2:1": "내 성능에\n너무 기대고\n있는 거 아니야?"
  },
  "6BC0C8": {
    "70:0": "쳇, 실수했나...\n하지만 다음에야말로!!",
    "71:0": "우오옷!\n속이 시원하네!!",
    "71:1": "기분 탓인지,\n힘이 솟아나는\n것 같군!",
    "72:0": "내 손에 걸리면,\n이 정도는 식은 죽 먹기지!",
    "72:1": "......\n응? 뭔가 데이터가\n도착한 모양이군",
    "72:2": "제니가\n전송됐어!\n이번 보수라는데",
    "72:3": "해냈어...!!",
    "73:0": "내 손에 걸리면,\n이 정도는 식은 죽 먹기지!",
    "73:1": "......\n응? 뭔가 데이터가\n도착한 모양이군",
    "73:2": "버그 조각이",
    "73:3": "개\n전송됐어!\n이번 보수라는데",
    "73:4": "해냈어...!!"
  },
  "6BC2F8": {
    "1:0": "플러그인!\n네이팜맨.EXE,\n트랜스미션!!"
  },
  "6BC74C": {
    "1:1": ",\n메일이 왔어!!",
    "2:1": ",\n메일이 왔어!!",
    "3:1": ",\n메일이 왔어!!",
    "4:1": "메일이 왔어!!",
    "5:1": "메일이 왔어!!",
    "6:1": "메일이 왔어!!",
    "7:1": "메일이 왔어!!",
    "10:1": ",\n파괴 지령이\n도착했어",
    "20:1": "메일이 왔어!!",
    "21:1": "메일이 왔어!!",
    "22:1": "메일이 왔어!!",
    "23:1": "메일이 왔어!!",
    "24:1": "메일이 왔어!!",
    "25:1": "메일이 왔어!!",
    "26:1": "메일이 왔어!!"
  },
  "6BCCD0": {
    "1:0": "이럴 수가!!",
    "1:1": "압도적인\n화력을 자랑하는\n이 내가...",
    "1:2": "이, 이, 이, 인정 못 해!\n절대로 인정 못 해!!",
    "2:0": "봤냐!!\n이게 내 화력이다!",
    "2:1": "화살이든 총이든\n가져와 봐!!",
    "2:2": "뭐가 오든\n모조리 태워 버릴 테니까",
    "10:0": ",\n참가 등록이 안 됐어!",
    "20:0": "드디어 때가\n왔군...\n쏴 버리겠어!!",
    "21:0": "드디어 때가\n왔군...\n쏴 버리겠어!!",
    "22:0": "드디어 때가\n왔군...\n쏴 버리겠어!!",
    "23:0": "드디어 때가\n왔군...\n쏴 버리겠어!!"
  },
  "6BCEB4": {
    "1:0": "야, 슬슬",
    "3:0": "일정의 시간이었지",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없어...",
    "11:2": " 부터\n",
    "12:0": "야!"
  },
  "6BFF50": {
    "1:0": "인터넷으로 가자!",
    "1:1": "주말에 열리는\n토너먼트까지\n못 기다리겠어",
    "1:2": "빨리 쏴 버리고 싶어서\n몸이 근질거린다고!",
    "2:0": "괜찮은 거지...\n마음껏\n쏴 버려도...",
    "2:1": "오늘 토너먼트에서,\n맞붙을 상대가\n불쌍하군...",
    "3:0": "야, 재미있어 보이는\n아이템이 있잖아",
    "3:1": "키 아이템을\n살펴봐!"
  },
  "6C04FC": {
    "1:0": "더 쏘게 해 줘!",
    "1:1": "난 아직도\n만족 못 했어!!",
    "2:0": "활활 타오르는 지옥불\n속에서 울려 퍼지는\n최후의 비명...",
    "2:1": "오직 그것만이 내\n메마른 마음을\n적셔 주지!!",
    "3:0": "어느 한쪽이 이길 때까지\n하게 해 달라고!"
  },
  "6C167C": {
    "1:0": "처음 뵙겠습니다!",
    "1:1": "저는 아이스맨이에요!\n아직 부족하지만,\n잘 부탁드려요",
    "2:0": "아이스맨 부활이에요~",
    "2:1": "열심히 힘낼 테니까,\n잘 부탁드려요!!"
  },
  "6C1B84": {
    "1:0": ",\n다녀왔어요~!",
    "1:1": "왠지 컨디션이\n좋은 것 같아요~!!",
    "2:0": "으~~...\n오늘은 조금\n더웠어요..."
  },
  "6C2368": {
    "1:1": " 방송이\n시작할 시간이에요~!",
    "1:2": "기대돼요~!!",
    "2:1": "\n일정의 시간이에요",
    "2:2": "마음껏\n즐길 거예요!!",
    "3:0": "식사 시간이에요!",
    "3:1": "저도,\n배가 고파요~!",
    "4:1": "학원 갈 시간이에요\n열심히 공부\n하세요!!",
    "5:1": " 일정의\n시간이에요~!",
    "6:0": "그리고...",
    "21:1": " 방송이\n시작할 시간이에요~!",
    "21:2": "기대돼요~!!",
    "22:1": "\n일정의 시간이에요",
    "22:2": "마음껏\n즐길 거예요!!",
    "23:0": "식사 시간이에요!",
    "23:1": "저도,\n배가 고파요~!",
    "24:1": "학원 갈 시간이에요\n열심히 공부\n하세요!!",
    "25:1": " 일정의\n시간이에요~!",
    "26:0": "그리고..."
  },
  "6C2D3C": {
    "1:0": "아, 맞아요!\n조금 있으면,",
    "3:0": "일정의 시간이에요!",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없어요",
    "11:2": " 부터\n",
    "12:0": "예요!"
  },
  "6C5994": {
    "1:0": "주말에 열리는\n토너먼트,\n기대돼요~!",
    "1:1": "아직 시간이 있어요!\n배틀 연습을\n해요!!",
    "2:0": "오늘 토너먼트에서,\n힘낼 거예요!",
    "2:1": "저는 아이스맨이지만,\n마음은 활활\n타오르고 있어요!!",
    "3:0": "왠지 두근거리는\n아이템을 가지고\n있는 것 같아요!",
    "3:1": "키 아이템을\n살펴봐요!"
  },
  "6C5F28": {
    "1:0": "더 차가운\n칩을 많이\n써 줬으면 좋겠어요~",
    "2:0": "지금이라면 뭐든지\n얼릴 수 있을\n것 같아요~",
    "3:0": "다음에는 확실히\n승부를\n가려요!"
  },
  "6C7084": {
    "1:0": "......\n난 일렉맨",
    "1:1": "나와 함께 짜릿한\n하루하루를 보내자...",
    "2:0": "오랜만이군",
    "2:1": "날 완전히\n잊어버린 줄\n알았어",
    "2:2": "어쨌든\n잘 부탁해"
  },
  "6C7594": {
    "1:0": "돌아왔다\n",
    "1:1": ",\n지치지 않았나?",
    "2:0": "내 전광석화 같은\n움직임이 통하지 않다니\n방심은 금물이군..."
  },
  "6D1068": {
    "1:0": "좀 더, 빛을...",
    "2:0": "플랜트맨,\n활짝 피었다!!",
    "3:0": "무승부라면,\n6할쯤 핀 꽃처럼\n만족스럽네..."
  },
  "6D2180": {
    "1:0": "흥, 원래라면\n어리석은 인간의\nPET 따위에",
    "1:1": "들어가는 일은\n있을 수 없지만...",
    "1:2": "이번에는 그저\n변덕일 뿐이다...",
    "2:0": "빨리 나를\n싸우게 해라...",
    "2:1": "내 파괴 충동을\n채워라..."
  },
  "6DD63C": {
    "1:0": "고객 여러분께",
    "2:0": "오피셜ML",
    "3:0": "다크로이드",
    "4:0": "오피셜ML",
    "5:0": "다크로이드 발견",
    "6:0": "오피셜ML",
    "7:0": "또 다른 1체의 다크로이드",
    "16:0": "오피셜",
    "17:0": "탭맨을 조심하세요",
    "18:0": "오피셜",
    "19:0": "다크로이드 암약!",
    "20:0": "오피셜",
    "21:0": "수수께끼의 오퍼레이터!",
    "22:0": "오피셜",
    "23:0": "오퍼레이터의 정체 확인!",
    "24:0": "오피셜",
    "25:0": "길거리 습격 사건 발생",
    "26:0": "오피셜",
    "27:0": "영하의 세계",
    "28:0": "오피셜",
    "29:0": "토너먼트 초대",
    "41:0": "제목:"
  },
  "6DD718": {
    "0:0": "관리 사무국",
    "1:0": "토너먼트 개최",
    "2:0": "관리 사무국",
    "3:0": "등록",
    "4:0": "관리 사무국",
    "5:0": "등록",
    "6:0": "관리 사무국",
    "7:0": "등록",
    "8:0": "관리 사무국",
    "9:0": "등록",
    "10:0": "관리 사무국",
    "11:0": "등록",
    "41:0": "제목:",
    "65:0": "제목:",
    "66:0": "삭제됨",
    "67:0": "삭제됨"
  },
  "6DD798": {
    "0:0": "오피셜 보스",
    "1:0": "오피셜 지령",
    "41:0": "제목:",
    "54:0": "오피셜 보스",
    "55:0": "너답지 않군",
    "56:0": "오피셜 보스",
    "57:0": "보수",
    "58:0": "오피셜 보스",
    "59:0": "제목 없음",
    "65:0": "제목:"
  },
  "6DD804": {
    "0:0": "총책",
    "1:0": "암살 의뢰",
    "41:0": "제목:",
    "54:0": "총책",
    "55:0": "제목 없음",
    "56:0": "총책",
    "57:0": "보수",
    "58:0": "총책",
    "59:0": "제목 없음",
    "65:0": "제목:"
  },
  "6DD91C": {
    "0:0": "다크 길드",
    "1:0": "파괴 의뢰",
    "2:0": "다크 길드",
    "3:0": "파괴 의뢰",
    "4:0": "다크 길드",
    "5:0": "파괴 의뢰",
    "6:0": "다크 길드",
    "7:0": "파괴 의뢰",
    "8:0": "다크 길드",
    "9:0": "파괴 의뢰",
    "10:0": "다크 길드",
    "11:0": "파괴 의뢰",
    "12:0": "다크 길드",
    "13:0": "파괴 의뢰",
    "14:0": "다크 길드",
    "15:0": "파괴 의뢰",
    "16:0": "다크 길드",
    "17:0": "파괴 의뢰",
    "18:0": "다크 길드",
    "19:0": "파괴 의뢰",
    "20:0": "다크 길드",
    "21:0": "파괴 의뢰",
    "22:0": "다크 길드",
    "23:0": "파괴 의뢰",
    "24:0": "다크 길드",
    "25:0": "파괴 의뢰",
    "26:0": "다크 길드",
    "27:0": "파괴 의뢰",
    "28:0": "다크 길드",
    "29:0": "파괴 의뢰",
    "41:0": "제목:",
    "65:0": "제목:"
  },
  "6DE2C8": {
    "0:0": "님",
    "0:1": "오늘 토너먼트에는 다음\n내비로 참가 등록을\n접수하였습니다",
    "1:0": "의 참가를\n",
    "1:1": "에서\n등록을 접수하였습니다",
    "2:0": "의 참가를\n",
    "2:1": "에서\n등록을 접수하였습니다",
    "3:0": "의 참가를\n",
    "3:1": "에서\n등록을 접수하였습니다",
    "4:0": "의 참가를\n",
    "4:1": "에서\n등록을 접수하였습니다",
    "5:0": "의 참가를\n",
    "5:1": "에서\n등록을 접수하였습니다",
    "31:0": "등록한 내비로,\n토너먼트 회장에\n와 주십시오",
    "33:0": "메일 본문이 없다...",
    "33:1": "이 메일은 시간이 되면\n자동으로 사라지도록\n되어 있는 것 같다..."
  },
  "6E2B9C": {
    "0:0": "   칩 폴더",
    "60:0": "칩 폴더를\n편집할 거야퓨",
    "61:0": "R 버튼에 배정할\n무기를 고르는 거야퓨",
    "62:0": "L 버튼에 배정할\n무기를 고르는 거야퓨",
    "70:0": "칩 폴더의 칩 수가\n",
    "70:1": "장으로 맞춰져 있지 않아퓨",
    "70:2": "편집을\n그만둘까퓨?\n",
    "70:3": "예  ",
    "70:4": "아니요",
    "71:0": "같은 칩은\n3장까지야퓨!",
    "72:0": "같은 메가 클래스 칩은\n1장만 넣을 수 있어퓨",
    "73:0": "같은 기가 클래스 칩은\n1장만 넣을 수 있어퓨",
    "74:0": "메가 클래스 칩은\n5장만 넣을 수 있어퓨",
    "75:0": "기가 클래스 칩은\n1장만 넣을 수 있어퓨"
  },
  "79C240": {
    "0:0": "100과 90의 S 조각을\n모은 자여...",
    "0:1": "지나가도 좋다...",
    "2:0": "100과 90의 S 조각이\n없는 자여...\n여기서 물러가라"
  },
  "79C518": {
    "0:0": "정말 멋진\n「",
    "0:1": "」...\n나도 모르게 합장하게 된다"
  },
  "79C554": {
    "0:0": "정말 멋진\n「",
    "0:1": "」...\n나도 모르게 합장하게 된다"
  },
  "79C590": {
    "0:0": "정말 멋진\n「",
    "0:1": "」...\n나도 모르게 합장하게 된다"
  },
  "79C5CC": {
    "0:0": "정말 멋진\n「",
    "0:1": "」...\n나도 모르게 합장하게 된다"
  },
  "79CB64": {
    "0:0": "정말 멋진\n「",
    "0:1": "」...\n나도 모르게 합장하게 된다",
    "1:0": "큰 나무로군...\n전뇌 세계에도 녹음이\n필요하다..."
  },
  "79CBCC": {
    "0:0": "큰 나무로군...\n전뇌 세계에도 녹음이\n필요하다..."
  },
  "79CC08": {
    "0:0": "정말 멋진\n「",
    "0:1": "」...\n나도 모르게 합장하게 된다"
  },
  "79CC44": {
    "0:0": "큰 나무로군...\n전뇌 세계에도 녹음이\n필요하다..."
  },
  "79CCB0": {
    "0:0": "정말 멋진\n「",
    "0:1": "」...\n나도 모르게 합장하게 된다",
    "1:0": "에브리데이 토너먼트,\n매일 개최!!",
    "1:1": "개최 시간은 매일",
    "1:4": "자신이야말로 최강이라\n자부하는 넷 배틀러들이여,\n모여라!!",
    "2:0": "에브리데이 토너먼트에\n온 걸 환영해!",
    "2:1": "자신이야말로 최강의\n넷 배틀러라고 자부하는",
    "2:2": "실력 좋은 내비들이\n준비를 완벽히 마치고\n기다리고 있어!!",
    "2:3": "너도 참가 등록할래?",
    "2:4": "예  ",
    "2:5": "아니요",
    "2:6": "좋아, 결정됐어!!\n자, 배틀이 시작된다!!",
    "2:7": "누가 최강의\n넷 배틀러인지,",
    "2:8": "네 실력으로\n증명해 봐!",
    "2:9": "에브리데이 토너먼트,\n스타아아아아아트!!",
    "3:0": "자신감이\n생기면 다시 와!",
    "4:0": "이번\n에브리데이 토너먼트는\n끝났어!",
    "4:1": "우승 축하한다!\n다음에도 출전해 줘!",
    "4:2": "개최 시간은 매일",
    "4:4": "PM4:00~PM5:00\nPM8:00~PM9:00\n야!!"
  },
  "7A7C04": {
    "0:0": "오늘은 쓰레기 버리는 날이네...\n수거 시간까지는\n아직 한참 남았으니,",
    "0:1": "오늘은 하드 디스크를\n대청소라도 해 볼까",
    "1:0": "내일은 화요일인가...\n그렇다면 불 속성의\n바이러스가 늘겠네...",
    "1:1": "난 불 속성이\n약점이니까, 플러그인은\n삼가야겠어..."
  },
  "7A7CF8": {
    "0:0": "오늘은 불 속성의\n바이러스가 유난히 많군",
    "0:1": "불 계열 칩을\n구하고 싶던 참이었으니,\n마침 잘됐어...",
    "1:0": "화재 주의보입니다!\n불에 약한 내비는\n주의해 주세요!!",
    "2:0": "화요일은 순찰하는 날이야",
    "2:1": "순찰이라고는 해도,\n일반 시민들과 교류하는 게\n가장 큰 목적이야",
    "3:0": "흠흠, 흠흠...\n...이상 없음!"
  },
  "7A7EF8": {
    "0:0": "나무 속성 바이러스를\n찾고 있어",
    "0:1": "칩은 사려면 비싸니까,\n되도록 바이러스를 쓰러뜨려\n얻고 있지",
    "1:0": "난 불 칩을\n잘 써!",
    "1:1": "그래서 오늘 같은 날은,\n바이러스를 마구 쓰러뜨리지!"
  },
  "7A8864": {
    "0:0": "뭐 좋은 거\n떨어진 게 없으려나...",
    "0:1": "가끔 쓰레기에 섞여서\n좋은 물건이 버려져\n있기도 하거든",
    "1:0": "쓰레기도 다 버렸고,\nPET 안도 한결\n깔끔해졌네",
    "1:1": "개운해, 개운해!"
  },
  "7A8AE0": {
    "0:0": "전기 속성인 분은\n너무 돌아다니지 않는 게\n좋아요~",
    "1:0": "왠지 나무 속성\n바이러스를 자주 만나네...",
    "1:1": "물 속성 바이러스를\n찾고 있는데\n오늘은 힘드려나"
  },
  "7A8E20": {
    "0:0": "헉, 헉, 헉, 헉...",
    "0:1": "토너먼트에 나가려고\n단련하고 있어!",
    "0:2": "다들 놀고 있을 때\n특훈을 해야,\n강해지는 법이지!!"
  },
  "7A99C0": {
    "0:0": "그러고 보니 오늘은 쓰레기 버리는 날이네\n나중에 버리러 가야겠다",
    "1:0": "있잖아, 알고 있어?\n프로그램 씨의\n데이터 일부는,",
    "1:1": "월요일에 버려지는\n쓰레기 데이터를 재활용해서\n만든대",
    "1:2": "쓰레기 데이터 안에는\n아직 쓸 수 있는 데이터도\n많이 들어 있거든",
    "1:3": "좀 놀랍지?"
  },
  "7A9BA0": {
    "0:0": "에에~, 싫어~!!",
    "0:1": "제발, 어떻게 좀!",
    "1:0": "오늘은 여자애면\n싸게 쇼핑할 수 있잖아?",
    "1:1": "부탁이야!\n내 것도 사다 줘!!",
    "1:2": "왜 내가\n너 따위를 위해서\n쇼핑해야 하는데!",
    "1:3": "그, 그러지 말고 제발!",
    "2:0": "인터넷8에 있는\n칩 상점,\n꽤 괜찮았어~",
    "2:1": "룰루룰루루~"
  },
  "7A9CAC": {
    "0:0": "아까 나무 속성 바이러스를\n「",
    "0:1": "」 칩으로\n쓰러뜨렸어!!",
    "0:2": "아주 잘 타더라고~!!",
    "1:0": "난 요일과\n바이러스 종류의\n관계에 대해",
    "1:1": "연구하고 있어",
    "1:2": "화요일은 불 속성\n수요일은 물 속성\n목요일은 나무 속성",
    "1:3": "그리고 금요일은\n전기 속성...",
    "1:4": "흠... 요일 이름 그대로네..."
  },
  "7A9DA8": {
    "0:0": "인터넷8에서\n친선 배틀을 한다나 봐!",
    "0:1": "너도 가 보지 그래?",
    "1:0": "인터넷8 쪽이\n시끄러운데,\n뭘 하고 있나?"
  },
  "7A9E44": {
    "0:0": "다들 주말에는\n토너먼트가 있다며\n떠들어 댔지만,",
    "0:1": "난 평화주의자라서,\n넷 배틀에는 관심이\n없거든"
  },
  "7AAB30": {
    "0:0": "내일부터는 다시 시끄러워질 테니\n지금 미리 느긋하게\n쉬어 둬야겠군..."
  },
  "7AABB0": {
    "0:0": "쓰레기를 버리러 가려고\n하는데,",
    "0:1": "인터넷6까지\n가지고 가기가 귀찮아",
    "0:2": "차라리 길 아래의\n전뇌 공간에...",
    "0:3": "안 돼! 그런 짓을 하면,\n전뇌법 제123조의",
    "0:4": "불법 투기 금지법에\n걸리고 말아!",
    "1:0": "아아, 또 한 주가\n시작됐어!!",
    "1:1": "힘드네..."
  },
  "7AACC0": {
    "0:0": "이 근처에는 혈기왕성한\n내비들이 자주 모이니까\n철저히 순찰해야 해!",
    "1:0": "최근에는 우리\n오피셜이 순찰을\n강화해서,",
    "1:1": "큰 사건은\n잘 일어나지 않게 됐어"
  },
  "7AAD84": {
    "0:0": "아직 숨겨 놓은 상품이\n있잖아요!!",
    "0:1": "꺼내 놓으세요!!",
    "0:2": "저, 정말 이제 없어요~!",
    "0:3": "거짓말하지 마세요!",
    "1:0": "뭐라도 덤으로 줘요!",
    "1:1": "좀 봐주세요\n손님~",
    "1:2": "저도 적자를 각오하고\n장사하는 거라니까요",
    "2:0": "저 상점 내비는\n내 남자 친구야...",
    "2:1": "수요일만 되면\n여자애들에게 둘러싸여서\n헤벌쭉, 헤벌쭉...",
    "2:2": "으이익!\n용서 못 해!!",
    "2:3": "...하지만,\n저것도 일의 일부니까...",
    "2:4": "딴마음 먹지 못하게\n여기서 눈에 힘을 주고 있는 거야"
  },
  "7AAEF0": {
    "0:0": "난 옛날에\n인터넷2에서",
    "0:1": "견습 넷 배틀러\n라이선스 시험의\n시험관을 맡았었지",
    "0:2": "아아, 그리운 시절이네"
  },
  "7AB420": {
    "0:0": "으음,\n주말은 조용해서 좋네",
    "0:1": "오늘은 조용히\n1초 1초, 시간의 흐름을\n느끼며 1일을 보낼 거야"
  },
  "7AD8D0": {
    "0:0": "청소, 청소!",
    "0:1": "저는 이 에리어의\n청소 담당\n프로그램입니다!",
    "0:2": "사람이 적은\n주말에 청소한 뒤,",
    "0:3": "월요일에 한꺼번에\n버립니다!!"
  },
  "7AD978": {
    "0:0": "인터넷11에 쓰레기를 버리러\n가야겠어",
    "0:1": "...귀찮네\n다음 주에 할까...",
    "1:0": "이 에리어에는\n파출소가 있어서,\n치안이 좋아!",
    "1:1": "언제나 안심하고\n인터넷에 올 수 있지!",
    "1:2": "그렇다고 해도, 난\n거의 월요일에만\n오지만 말이야"
  },
  "7ADA60": {
    "0:0": "딱 봐도 나쁜 짓을 할 것 같은\n얼굴이군...",
    "0:1": "뭔가 저질렀지!",
    "0:2": "아, 아무 짓도 안 했어!",
    "0:3": "내가 이런 모습이긴\n하지만 말이야,",
    "0:4": "지금까지 단 한 번도\n하늘을 우러러 부끄러워할\n짓은 하지 않았다고!!",
    "1:0": "그러니까, 난 아무 짓도\n안 했다니까!!",
    "1:1": "대체 너는,\n지난주에도 똑같은 말을\n했잖아!!",
    "1:2": "이제 좀 기억해 달라고!",
    "1:3": "수상한 얼굴을 하고 있는\n네가 잘못이지!"
  }
}
EXCLUDED={"6BC0C8:0:0","79C240:1:0"}
CHOICES=set(["6E2B9C:70:3","6E2B9C:70:4","79CCB0:2:4","79CCB0:2:5"])
LABELS=set(["6DD63C:1:0","6DD63C:2:0","6DD63C:3:0","6DD63C:4:0","6DD63C:5:0","6DD63C:6:0","6DD63C:7:0","6DD63C:16:0","6DD63C:17:0","6DD63C:18:0","6DD63C:19:0","6DD63C:20:0","6DD63C:21:0","6DD63C:22:0","6DD63C:23:0","6DD63C:24:0","6DD63C:25:0","6DD63C:26:0","6DD63C:27:0","6DD63C:28:0","6DD63C:29:0","6DD63C:41:0","6DD718:0:0","6DD718:1:0","6DD718:2:0","6DD718:3:0","6DD718:4:0","6DD718:5:0","6DD718:6:0","6DD718:7:0","6DD718:8:0","6DD718:9:0","6DD718:10:0","6DD718:11:0","6DD718:41:0","6DD718:65:0","6DD718:66:0","6DD718:67:0","6DD798:0:0","6DD798:1:0","6DD798:41:0","6DD798:54:0","6DD798:55:0","6DD798:56:0","6DD798:57:0","6DD798:58:0","6DD798:59:0","6DD798:65:0","6DD804:0:0","6DD804:1:0","6DD804:41:0","6DD804:54:0","6DD804:55:0","6DD804:56:0","6DD804:57:0","6DD804:58:0","6DD804:59:0","6DD804:65:0","6DD91C:0:0","6DD91C:1:0","6DD91C:2:0","6DD91C:3:0","6DD91C:4:0","6DD91C:5:0","6DD91C:6:0","6DD91C:7:0","6DD91C:8:0","6DD91C:9:0","6DD91C:10:0","6DD91C:11:0","6DD91C:12:0","6DD91C:13:0","6DD91C:14:0","6DD91C:15:0","6DD91C:16:0","6DD91C:17:0","6DD91C:18:0","6DD91C:19:0","6DD91C:20:0","6DD91C:21:0","6DD91C:22:0","6DD91C:23:0","6DD91C:24:0","6DD91C:25:0","6DD91C:26:0","6DD91C:27:0","6DD91C:28:0","6DD91C:29:0","6DD91C:41:0","6DD91C:65:0","6E2B9C:0:0"])
CONTEXT={
  "69EF48": "Wood tournament/outcome; earth gratitude and overly gentle operator. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6A26C8": "Wood tournament/outcome; earth gratitude and overly gentle operator. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6A383C": "Star greetings/return/comet/sixth-magnitude brightness, hesitant plugin, shooting-star wish, win/loss/draw star wordplay and schedules. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6A3D48": "Star greetings/return/comet/sixth-magnitude brightness, hesitant plugin, shooting-star wish, win/loss/draw star wordplay and schedules. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6A4BF0": "Star greetings/return/comet/sixth-magnitude brightness, hesitant plugin, shooting-star wish, win/loss/draw star wordplay and schedules. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6A5578": "Star greetings/return/comet/sixth-magnitude brightness, hesitant plugin, shooting-star wish, win/loss/draw star wordplay and schedules. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6A570C": "Star greetings/return/comet/sixth-magnitude brightness, hesitant plugin, shooting-star wish, win/loss/draw star wordplay and schedules. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6A8A08": "Star greetings/return/comet/sixth-magnitude brightness, hesitant plugin, shooting-star wish, win/loss/draw star wordplay and schedules. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6A907C": "Star greetings/return/comet/sixth-magnitude brightness, hesitant plugin, shooting-star wish, win/loss/draw star wordplay and schedules. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6AA1A0": "Shadow samurai greeting/return, assassination mail9216 flags3613/3784 and tournament preparation/outcomes; nine-syllable incantation and mental focus candidate. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6AA6A0": "Shadow samurai greeting/return, assassination mail9216 flags3613/3784 and tournament preparation/outcomes; nine-syllable incantation and mental focus candidate. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6AAEB0": "Shadow samurai greeting/return, assassination mail9216 flags3613/3784 and tournament preparation/outcomes; nine-syllable incantation and mental focus candidate. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6AB458": "Shadow samurai greeting/return, assassination mail9216 flags3613/3784 and tournament preparation/outcomes; nine-syllable incantation and mental focus candidate. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6AE758": "Shadow samurai greeting/return, assassination mail9216 flags3613/3784 and tournament preparation/outcomes; nine-syllable incantation and mental focus candidate. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6AED8C": "Shadow samurai greeting/return, assassination mail9216 flags3613/3784 and tournament preparation/outcomes; nine-syllable incantation and mental focus candidate. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6B5FB0": "Knight formal return, plugin, tournament battle chant, training and tactics praise/caution. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6B60F0": "Knight formal return, plugin, tournament battle chant, training and tactics praise/caution. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6B69A0": "Knight formal return, plugin, tournament battle chant, training and tactics praise/caution. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6BA2BC": "Knight formal return, plugin, tournament battle chant, training and tactics praise/caution. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6BA910": "Knight formal return, plugin, tournament battle chant, training and tactics praise/caution. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6BBAF8": "Napalm explosive greeting/return, poor chip timing, minigame2 results/global5, HP33/1, zenny/bugfragments sentinel4294967295/buffer3, destruction mail and mission calls, tournament/outcomes. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6BC034": "Napalm explosive greeting/return, poor chip timing, minigame2 results/global5, HP33/1, zenny/bugfragments sentinel4294967295/buffer3, destruction mail and mission calls, tournament/outcomes. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6BC0C8": "Napalm explosive greeting/return, poor chip timing, minigame2 results/global5, HP33/1, zenny/bugfragments sentinel4294967295/buffer3, destruction mail and mission calls, tournament/outcomes. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6BC2F8": "Napalm explosive greeting/return, poor chip timing, minigame2 results/global5, HP33/1, zenny/bugfragments sentinel4294967295/buffer3, destruction mail and mission calls, tournament/outcomes. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6BC74C": "Napalm explosive greeting/return, poor chip timing, minigame2 results/global5, HP33/1, zenny/bugfragments sentinel4294967295/buffer3, destruction mail and mission calls, tournament/outcomes. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6BCCD0": "Napalm explosive greeting/return, poor chip timing, minigame2 results/global5, HP33/1, zenny/bugfragments sentinel4294967295/buffer3, destruction mail and mission calls, tournament/outcomes. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6BCEB4": "Napalm explosive greeting/return, poor chip timing, minigame2 results/global5, HP33/1, zenny/bugfragments sentinel4294967295/buffer3, destruction mail and mission calls, tournament/outcomes. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6BFF50": "Napalm explosive greeting/return, poor chip timing, minigame2 results/global5, HP33/1, zenny/bugfragments sentinel4294967295/buffer3, destruction mail and mission calls, tournament/outcomes. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6C04FC": "Napalm explosive greeting/return, poor chip timing, minigame2 results/global5, HP33/1, zenny/bugfragments sentinel4294967295/buffer3, destruction mail and mission calls, tournament/outcomes. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6C167C": "Ice polite awkward greeting/return, heat weakness, schedule reminder quick versus explicit IceMan21..26, cold chips and burning heart. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6C1B84": "Ice polite awkward greeting/return, heat weakness, schedule reminder quick versus explicit IceMan21..26, cold chips and burning heart. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6C2368": "Ice polite awkward greeting/return, heat weakness, schedule reminder quick versus explicit IceMan21..26, cold chips and burning heart. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6C2D3C": "Ice polite awkward greeting/return, heat weakness, schedule reminder quick versus explicit IceMan21..26, cold chips and burning heart. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6C5994": "Ice polite awkward greeting/return, heat weakness, schedule reminder quick versus explicit IceMan21..26, cold chips and burning heart. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6C5F28": "Ice polite awkward greeting/return, heat weakness, schedule reminder quick versus explicit IceMan21..26, cold chips and burning heart. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6C7084": "Elec stimulating reunion/return and lightning movement caution. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6C7594": "Elec stimulating reunion/return and lightning movement caution. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6D1068": "Plant battle outcomes: more light, full bloom, sixth-tenths bloom satisfaction. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6D2180": "Bass contempt for human PET, whim and destructive impulse; no explicit local portrait. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6DD63C": "Story mail sender/title labels; I.P.C. preserved, OfficialML/Official, Darkloid discovery/identity/ambush and TapMan warnings. Not dialogue. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6DD718": "Tournament administration sender/title labels with printMailBuffer before registration suffix, deleted states distinct. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6DD798": "Official boss mission sender/titles, failure/reward/untitled labels distinct. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6DD804": "Assassination broker sender/title labels; 총책 is an unapproved referent wording candidate. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6DD91C": "Dark Guild sender/destruction-request labels,30alternating sender/title slots and generic title prefixes. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6DE2C8": "Tournament registration mail: SciLabMan0..5, buffered Navi then tournament, registeredNavi invitation31 inherited source jump chain, blank/auto-expiring mail33 no explicit portrait. Dynamic noun particles invariant. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "6E2B9C": "Aqua folder label0, quick hints60..62, explicit Aqua70..75. R/L equipment selection, dynamic folder count, yes/no width8, samechip3, sameMega/Giga1, totalMega5/Giga1; not new gameplay rules. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "79C240": "S fragments100and90/source standard library190 gate; native flag1736. Placeholder BugPieceTrader(temporary) unselected unresolved. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "79C518": "Anonymous statue/item7 admiration and tree greenery in cyberworld; no portrait inferred. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "79C554": "Anonymous statue/item7 admiration and tree greenery in cyberworld; no portrait inferred. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "79C590": "Anonymous statue/item7 admiration and tree greenery in cyberworld; no portrait inferred. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "79C5CC": "Anonymous statue/item7 admiration and tree greenery in cyberworld; no portrait inferred. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "79CB64": "Anonymous statue/item7 admiration and tree greenery in cyberworld; no portrait inferred. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "79CBCC": "Anonymous statue/item7 admiration and tree greenery in cyberworld; no portrait inferred. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "79CC08": "Anonymous statue/item7 admiration and tree greenery in cyberworld; no portrait inferred. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "79CC44": "Anonymous statue/item7 admiration and tree greenery in cyberworld; no portrait inferred. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "79CCB0": "EverydayTournament7 time09/13/16/20, purpleHeel host, choice hidden width8/default0, flag1929/7736, item7 statue; source time-only literals preserved. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A7C04": "NPC weekday trash/patrol/elemental viruses/fire warning/chip collection/training/recycled program-data rumor; explicit individual portraits preserved. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A7CF8": "NPC weekday trash/patrol/elemental viruses/fire warning/chip collection/training/recycled program-data rumor; explicit individual portraits preserved. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A7EF8": "NPC weekday trash/patrol/elemental viruses/fire warning/chip collection/training/recycled program-data rumor; explicit individual portraits preserved. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A8864": "NPC weekday trash/patrol/elemental viruses/fire warning/chip collection/training/recycled program-data rumor; explicit individual portraits preserved. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A8AE0": "NPC weekday trash/patrol/elemental viruses/fire warning/chip collection/training/recycled program-data rumor; explicit individual portraits preserved. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A8E20": "NPC weekday trash/patrol/elemental viruses/fire warning/chip collection/training/recycled program-data rumor; explicit individual portraits preserved. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A99C0": "NPC weekday trash/patrol/elemental viruses/fire warning/chip collection/training/recycled program-data rumor; explicit individual portraits preserved. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A9BA0": "Wednesday shopping: Orangegirl refuses purpleHeel purchase favor; pink shopper likesInternet8. Distinct speakers. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A9CAC": "Yellow uses printChip12 to defeat woodvirus; Official weekday-element research joke, no added mechanical cause. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A9DA8": "Internet8 informalbattle report/question versus peaceful no-interest and rest before noisy weekdays. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7A9E44": "Internet8 informalbattle report/question versus peaceful no-interest and rest before noisy weekdays. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7AAB30": "Internet8 informalbattle report/question versus peaceful no-interest and rest before noisy weekdays. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7AABB0": "Official trash temptation rejected by fictitious cyberlaw123, patrol intensified; yellow start-of-week fatigue. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7AACC0": "Official trash temptation rejected by fictitious cyberlaw123, patrol intensified; yellow start-of-week fatigue. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7AAD84": "Orangegirl bargains with yellow merchant, pink demands extra then envies her merchant boyfriend/watchesWednesdaygirls; no mixed dialogue. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7AAEF0": "Official former Internet2 trainee-license examiner nostalgia and quietweekend1second/1day. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7AB420": "Official former Internet2 trainee-license examiner nostalgia and quietweekend1second/1day. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7AD8D0": "Green cleaning program/weekend then Mondaydump; PurpletrashInternet11/Yellowpoliceboxsafety; Official accusespurpleHeel who denies wrongdoing and pointsoutrepeatlastweek. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7AD978": "Green cleaning program/weekend then Mondaydump; PurpletrashInternet11/Yellowpoliceboxsafety; Official accusespurpleHeel who denies wrongdoing and pointsoutrepeatlastweek. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified.",
  "7ADA60": "Green cleaning program/weekend then Mondaydump; PurpletrashInternet11/Yellowpoliceboxsafety; Official accusespurpleHeel who denies wrongdoing and pointsoutrepeatlastweek. IDs/source/TPL/payload, native commands/values/branches/variables/portraits, newline/padding immutable. Actual consumer geometry/reachability and semantic approval remain unverified."
}
SEMANTIC_REVIEW=[
  "Exactly500 stable catalog literals across76archives:366Navi/mail/folder and134NPC/statue/gate/tournament. All500sources, native skeletons and adjacent unselected literals inspected; repeated native blocks read by exact equivalent templates. Not500 unique sentences.",
  "Manually authored source-conditioned free prose, no rule-based prose generation/choice/shortening. Allneeds_review development-draft NON-DISTRIBUTION releasefalse. New terms/voices/wordplay need human review.",
  "Quick speech has no explicit portrait unless local mugshotShow; self-intro is textual context not proof of actual runtime routing. IceMan21..26, AquaMan70..75, SciLabMan0..5 and distinct NPC portrait switches preserved;31SciLabMan inherited from0 jump chain,33unknown.",
  "Star source win/loss white/black stars and gray-star draw joke retains explicit outcomes; sixth-magnitude dimness differs from Plant six-tenths bloom. Shadow nine voiced incantation syllables and samurai register, Knight battle chant, Napalm harsh speech, Ice awkward politeness are review candidates.",
  "Four native choices,91labels including90mail labels and1folder label; labels not spoken. Folder70dynamiccount and constraints3/1/1/5/1 immutable; same-class duplicate limits distinct from total class count.",
  "Dynamic nickname/Navi/tournament/schedule/chip/item/buffer particles and inline flow require actual consumer review. Source gate100and90 references standard190 checks, not fabricated collectible count changes. Law123 is in-game fiction, not real legal advice.",
  "Source temporary6BC0C8:0:0 and79C240:1:0 retained unresolved inremaining denominator; SP temporary trader79C8D8 also deferred. No debug/glyph tables declared complete or silently excluded.",
  "Mail labels need consumer width/layout review; existing mail bodies and folder equipment labels are preserved. Statuename/item7, no inferred narrator portrait. Source digitalgreenery, firewarning and recycledprogram-data rumor retain confidence level.",
  "Codec/glyph/skeleton/protectedfields/132px heuristic passes do not constitute semantic/human/runtime approval. Allremainingdrafts first, then cumulative insertion/font/consumer readiness and ROM screen/saveQA; keyboard/persistence/graphics/release remainopen. No ROM/save/emulator writes."
]
def authored(archive):return DRAFT[archive]
def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    plan=json.loads((ROOT/'translations/full_translation_first_plan.json').read_text(encoding='utf8'))
    require_hash(ROOT/plan['source_inventory']['path'],plan['source_inventory']['sha256'])
    catalog=json.loads((ROOT/plan['source_inventory']['path']).read_text(encoding='utf8'))
    remaining={u['id'] for u in catalog['units'] if u['archive']==archive and u['status']=='unselected_japanese'}
    ids={archive+':'+k for k in authored(archive)}
    if not ids<=remaining or ids & EXCLUDED:raise ValueError('batch selected-ID scope '+archive)
    values={archive+':'+k:v for k,v in authored(archive).items()}
    selected=[x for x in literals(original) if x.key in ids]
    if len(selected)!=count or set(values)!=ids:raise ValueError('batch scope '+archive+' missing '+str(ids-set(values))+' extra '+str(set(values)-ids))
    units=[]
    scripts={int(m.group(1)):m.group(2) for m in re.finditer(r'script (\d+) \w+ \{(.*?)(?=\nscript |\Z)',original,re.S)}
    for x in selected:
        suffix=':'.join(x.key.split(':')[1:]);t=values[x.key];s=int(suffix.split(':')[0])
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('batch topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('batch tokens '+x.key)
        if len(x.text)-len(x.text.rstrip(' '))!=len(t)-len(t.rstrip(' ')):raise ValueError('batch padding '+x.key)
        if len(x.text)-len(x.text.lstrip(' '))!=len(t)-len(t.lstrip(' ')):raise ValueError('batch leadingpadding '+x.key)
        if any(len(src)-len(src.lstrip(' '))!=len(dst)-len(dst.lstrip(' ')) for src,dst in zip(x.text.split('\n'),t.split('\n'))):raise ValueError('batch perline leadingpadding '+x.key)
        prefix=original[original.index('script '+str(s)+' '):x.start]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',prefix))
        portrait=events[-1].group(1) if events and events[-1].group(1) else None
        visibility='shown' if portrait else 'hidden' if events else 'not-shown-in-script'
        speaker_evidence='explicit local portrait' if portrait else 'unestablished local speaker'
        if x.key in LABELS:
            speaker='ui-label';speaker_evidence='native mmbn45s label; not spoken dialogue or choice'
        elif x.key in CHOICES:
            speaker='player-choice';speaker_evidence='native option literal'
        else:
            speaker=portrait or 'speaker-unestablished'
            if archive=='6DE2C8' and s==31:
                speaker='SciLabMan';speaker_evidence='source jump from0 inherits SciLabMan; not local portrait or runtime evidence'
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait=portrait,portrait_visibility=visibility,speaker_evidence=speaker_evidence,context=CONTEXT[archive],
            variable_context='Native dynamic inserts/branch/choice/portrait/HP commands immutable; inline grammar/geometry/reachability/runtime unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='batch500-contextual-navi-mail-npcs',
        context=CONTEXT[archive],voice='Manual source-conditioned drafts;explicit portrait where shown;unapproved terms and voices.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Source IDs/text/TPL/payload,commands,variables,newline/padding and unselected source immutable; no ROM/save writes.',
        batch_id='batch500-045',semantic_review=SEMANTIC_REVIEW,units=units)

def main():
    if sum(v[1] for v in SOURCES.values())!=500:raise ValueError('500 batch size')
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve batch asset '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()

