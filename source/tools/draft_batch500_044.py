"""500 manual contextual Navi greeting/reminder/result drafts; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
    "65E828": ["b3aca06439c4e20f018a3f422315826c2de70f96a9ac3e3a3a13fbe7a276c8ca",3,"translations/batch500_044_navi_alerts_65E828_draft_ko.json"],
    "66B8B0": ["d018ad4122672112ed27656854681b36fb7abe7cd05f7375a0228eaf6cc454de",4,"translations/batch500_044_navi_alerts_66B8B0_draft_ko.json"],
    "66F6A0": ["c2eb4d2985c264d91f692c96ba7051fbf00c12b71d6d3c341d1a86b57417d3a4",7,"translations/batch500_044_navi_alerts_66F6A0_draft_ko.json"],
    "66FC98": ["dee73611fe3012a8f33c78c5f7bb23ead98abda478ff04320b10a3f9c0a04ff0",4,"translations/batch500_044_navi_alerts_66FC98_draft_ko.json"],
    "670DF4": ["f0b4cc0f5f8a4941969b188af45dd5f7d77d351700288b8aa8f54cf56bb2dfa5",5,"translations/batch500_044_navi_alerts_670DF4_draft_ko.json"],
    "67133C": ["e50628722cc65285f7198c919e6ae1dd83d31df27f2d9fb81a686caff414fd7f",3,"translations/batch500_044_navi_alerts_67133C_draft_ko.json"],
    "672124": ["d282034ab96d11e6fb763dee4bebd94721fe208e121bae6b54024fdec356f523",6,"translations/batch500_044_navi_alerts_672124_draft_ko.json"],
    "675338": ["702dc7bc8832bf853389805f5caf6dc83e9f2220cef213c07fc9fcfa0e1a0795",7,"translations/batch500_044_navi_alerts_675338_draft_ko.json"],
    "67593C": ["1356b6b8691b9d90b60e2555bebebdcb63c8a4898b9d1aad615e9606737ab9a3",7,"translations/batch500_044_navi_alerts_67593C_draft_ko.json"],
    "676AE4": ["71cae9929b313d72a8c22c40d203054b58f04a76e87fd25c880303e075bc6726",6,"translations/batch500_044_navi_alerts_676AE4_draft_ko.json"],
    "677028": ["d0a77fd0171549161ce48469e13f48dcf9bbaf600d74061a5be460b781e89252",4,"translations/batch500_044_navi_alerts_677028_draft_ko.json"],
    "6770B8": ["cd1e4921477196d4d1483472af6f755e4ca9d999e27d9401b3a72867a9a04443",17,"translations/batch500_044_navi_alerts_6770B8_draft_ko.json"],
    "677774": ["d99950948e961608ddbfd4646dbeac0f3758e337579141340d85180b9b17c46a",14,"translations/batch500_044_navi_alerts_677774_draft_ko.json"],
    "677C94": ["89d72f5d9390d6f67b136e18a716d380ded601ce62beef028c7f6e1e47ae872a",10,"translations/batch500_044_navi_alerts_677C94_draft_ko.json"],
    "677E58": ["8d4292a472c28bb410cc69057449f26277c2bd3e1b7bea658e92ad2f1a17bbdf",6,"translations/batch500_044_navi_alerts_677E58_draft_ko.json"],
    "67AD3C": ["e78ca74a999e1eb8b2c424f54efd0a470652ad36c9857dcd4c00756a67458e73",7,"translations/batch500_044_navi_alerts_67AD3C_draft_ko.json"],
    "67B3D0": ["9223aa3400541e7ff4775f099cfdb2e55b57535b26264d04d335b58a3cdbacce",4,"translations/batch500_044_navi_alerts_67B3D0_draft_ko.json"],
    "67C4CC": ["d49a533c09d0b1efab4d1e6d04d6f5ac26d50c8f3f4625d3800258332757c946",5,"translations/batch500_044_navi_alerts_67C4CC_draft_ko.json"],
    "67C9FC": ["7196b80171a6c7f5ba67fd6cbf82700f8a92861837f8318eea0d4366366c2a62",3,"translations/batch500_044_navi_alerts_67C9FC_draft_ko.json"],
    "67CB24": ["f30730850ddbb1b7d69c61687a9615448f86a67a635c9c57092c582c13a238c8",1,"translations/batch500_044_navi_alerts_67CB24_draft_ko.json"],
    "67CED8": ["35666060cd2d1fee3fb4895795e5904ea20c77125623013e3fbfef3c2fa22a34",14,"translations/batch500_044_navi_alerts_67CED8_draft_ko.json"],
    "67D44C": ["6cb384731feb097231e5e5d26344678a36d722c3723b3443741541837807770e",9,"translations/batch500_044_navi_alerts_67D44C_draft_ko.json"],
    "67D5F8": ["003ee2f836e37cd09f8ee34f4d2f10d7a8661001d01ab926bf8a94d5c65b261d",6,"translations/batch500_044_navi_alerts_67D5F8_draft_ko.json"],
    "680370": ["7ce9615840affd4400603ecb1202f7a27f63a6a5c07876f0dab309d4b913e73a",6,"translations/batch500_044_navi_alerts_680370_draft_ko.json"],
    "6808C4": ["c4efba0b7b3ccc49aa866c93be59484849c02ce671379e671a1f7f488d735a73",4,"translations/batch500_044_navi_alerts_6808C4_draft_ko.json"],
    "681AB8": ["a5134d2b3c023a48796e0404170362fc4ff5633b327d715990fbad4d709b4ef2",5,"translations/batch500_044_navi_alerts_681AB8_draft_ko.json"],
    "681FD4": ["7913972779e3d2225e85a8c331bf51127a6c4bee455d8965e7a9deda9edd7811",4,"translations/batch500_044_navi_alerts_681FD4_draft_ko.json"],
    "682054": ["0b0f6938621117342b1075db31183bdf11fdaa869e91ecdfe6b14271eca8bb63",28,"translations/batch500_044_navi_alerts_682054_draft_ko.json"],
    "6824B8": ["604764f0d93fb869748720db000d6f06bc499232ea411ed44e3d34384e3a4464",1,"translations/batch500_044_navi_alerts_6824B8_draft_ko.json"],
    "682504": ["a285a790bedd9a4ede16b7f9a6518de6398063fb6d3ad329a401fe3433fa611e",16,"translations/batch500_044_navi_alerts_682504_draft_ko.json"],
    "6827F8": ["510cdf25c2b109706f0ea1e5c96f82e315a236555550243ef1a0ce647cc6cd68",15,"translations/batch500_044_navi_alerts_6827F8_draft_ko.json"],
    "682D68": ["4d52cea27fd00299987beb45bc53289c66f38aa048196244b6630cfbf35fa549",9,"translations/batch500_044_navi_alerts_682D68_draft_ko.json"],
    "682F44": ["9516a4e258227474dc452d3ee6d0eb0111141c9e5dddd193e3cce4922bd5436d",5,"translations/batch500_044_navi_alerts_682F44_draft_ko.json"],
    "685B7C": ["dcd572caf24f35dd4d75cc85dbc047e3ab22cb59a6dfabeb07cd68956d097b67",6,"translations/batch500_044_navi_alerts_685B7C_draft_ko.json"],
    "68611C": ["e62521938ef2eb7e45fae208dd00721059525cc776c388f90d663ec0cb5ba000",3,"translations/batch500_044_navi_alerts_68611C_draft_ko.json"],
    "68787C": ["2ce3b45cb4aff5ccacccbf3f06271948d9f8f65e0f76c593051a9766b7dedcd9",4,"translations/batch500_044_navi_alerts_68787C_draft_ko.json"],
    "688900": ["8bb0eb867abbea9b031e2a021d6d1824fb7cd8193c74bfd2c5ed4ee1a4e5b339",6,"translations/batch500_044_navi_alerts_688900_draft_ko.json"],
    "68BAAC": ["b84556fec6ee4f3384aa13a11fdb9ed901fa8da13b9d658f941158b86afccee2",8,"translations/batch500_044_navi_alerts_68BAAC_draft_ko.json"],
    "68C2CC": ["8033e6ac9dd625b025e63844b3d8bdaf16d6d52311cc397c0b5fc2403004d900",4,"translations/batch500_044_navi_alerts_68C2CC_draft_ko.json"],
    "68D3C8": ["ace284326a28637ae890624e923432c6d58e9fc8c282b2a8dcc2c81724de45f2",4,"translations/batch500_044_navi_alerts_68D3C8_draft_ko.json"],
    "68D8F8": ["401ad01c3d458da46b8ac2d87eb7467d8d29e03eec24b681fd4009f42feb0d02",2,"translations/batch500_044_navi_alerts_68D8F8_draft_ko.json"],
    "68DD4C": ["c6de1986a5d19baab2f11ff4a0237c9249784f123da00849753ef343d63a713c",1,"translations/batch500_044_navi_alerts_68DD4C_draft_ko.json"],
    "68DD98": ["d469ff29cd2d0d34256442e670f290a81723f11345f0861abf298bfddb1034ac",20,"translations/batch500_044_navi_alerts_68DD98_draft_ko.json"],
    "68E7BC": ["043851958e012672c9545f39b9a2995fc1b60bff12014afaa149f7ab70d5d0e2",6,"translations/batch500_044_navi_alerts_68E7BC_draft_ko.json"],
    "691994": ["50655c51819087bd60d458b43c613a0f26fdcd7d08d8d4478591d20e44ae6f00",5,"translations/batch500_044_navi_alerts_691994_draft_ko.json"],
    "691F80": ["158e4c674d1d7ce95049fee955ed503ffc2e928f9ad5930beed990b8ecf0d248",4,"translations/batch500_044_navi_alerts_691F80_draft_ko.json"],
    "69303C": ["2f7799d8c1a7559736d342738d1c68d691f0bb782fa073e8b9a78586e5121e05",6,"translations/batch500_044_navi_alerts_69303C_draft_ko.json"],
    "693590": ["1c1497ba77757519d0bf14d3902841c009946f1029bd71e10b5a1d4380ae021f",3,"translations/batch500_044_navi_alerts_693590_draft_ko.json"],
    "693778": ["a514bf1e4a1ca0e8ad7f98a9feb2f0584a006801e924a03a501fe1e7afe013d7",1,"translations/batch500_044_navi_alerts_693778_draft_ko.json"],
    "6941DC": ["133d482c71feb791a63a56c8ffadf4c1583077f63a1e3505e923fdabad6bc08d",6,"translations/batch500_044_navi_alerts_6941DC_draft_ko.json"],
    "696CF4": ["2e01acc0a7405eb2186f0c800556661c425fbc8c06c621fb32bde909971319f1",7,"translations/batch500_044_navi_alerts_696CF4_draft_ko.json"],
    "697268": ["a3947efab04d427bacca8507b622593928e189cb138d2ce86b4a52996a8f0d3a",4,"translations/batch500_044_navi_alerts_697268_draft_ko.json"],
    "6989B0": ["4d7db2d277a81dfa021486547f0220e646f876fa6312bfd6675878126eb708be",2,"translations/batch500_044_navi_alerts_6989B0_draft_ko.json"],
    "698A2C": ["d5925f1c41c14a33bbe98d16985f3b6be5b45f558e6ac0e7548bc6e911940a73",14,"translations/batch500_044_navi_alerts_698A2C_draft_ko.json"],
    "698CB0": ["70f9faf36ba04d94173011f7b00b54b6db40ab3de776e551eea187d0f7bbcfc6",1,"translations/batch500_044_navi_alerts_698CB0_draft_ko.json"],
    "698CFC": ["40dff0c0cb391ac3da35cb6299231897708556f658f71c534a2288bfc219a0fd",56,"translations/batch500_044_navi_alerts_698CFC_draft_ko.json"],
    "699194": ["ff320e84143fae8c8ee80a6b665cf44f52d7e4ca8f87996548c4675a763cc334",14,"translations/batch500_044_navi_alerts_699194_draft_ko.json"],
    "6996DC": ["26c81f91134db47d8bac527e73c967e18c6e669636b16af81a5bed7acedf410a",10,"translations/batch500_044_navi_alerts_6996DC_draft_ko.json"],
    "6998DC": ["02a440b6e1f0cbf7a0ba7021618449532cb698db65edefb94a25a8f504a348bd",6,"translations/batch500_044_navi_alerts_6998DC_draft_ko.json"],
    "69C8FC": ["8ceb97e4477e12efa2df38f8aa4104d1b2f6868f9ffae3d7a4b22f7061d2ff28",6,"translations/batch500_044_navi_alerts_69C8FC_draft_ko.json"],
    "69CF44": ["47df8cc3ea2324ce74728d99dd5c89487f5f277d3fe4cb397bbcfe9d797a74a4",5,"translations/batch500_044_navi_alerts_69CF44_draft_ko.json"],
    "69E088": ["13a462c1fcbd19c2f6dcf03cb4b367808f427dc90c20d3e9ae6fd47963017da0",5,"translations/batch500_044_navi_alerts_69E088_draft_ko.json"],
    "69E5A8": ["400f3297b363a13580f670a6f23935df0c5177f7d2a9760bcd0959975d3a563e",2,"translations/batch500_044_navi_alerts_69E5A8_draft_ko.json"],
    "69E6BC": ["18c0c03f2e9080ecc884c150d6c671ad438402c8bc6a531740639378fbca1d86",1,"translations/batch500_044_navi_alerts_69E6BC_draft_ko.json"],
    "69E708": ["f03de1a33062903fcf8733eef33209610418047c9bdb28c3364f66243a4a4f9b",20,"translations/batch500_044_navi_alerts_69E708_draft_ko.json"],
    "69F11C": ["33794396ba0b1f48f31fe858af69c8cc534c03dc3d27b9d887d8ec44bc730ee6",6,"translations/batch500_044_navi_alerts_69F11C_draft_ko.json"],
    "6A207C": ["873ece979f28e591227b15fe60f9012407dce2abb33d47ac52d6b5cc0577d9ca",7,"translations/batch500_044_navi_alerts_6A207C_draft_ko.json"]
}
DRAFT={
  "672124": {
    "1:0": "그러고 보니 슬슬",
    "3:0": "일정의 시간이\n다가오고 있습니다",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없습니다...",
    "11:2": " 부터\n",
    "12:0": "입니다"
  },
  "675338": {
    "1:1": "주말의\n토너먼트를 위해,\n특훈하시죠",
    "1:2": "승리를 거둘\n확률을 높이려면",
    "1:3": "매일 갈고닦는 것 외에\n방법이 없으니까요",
    "2:0": "오늘 토너먼트에서\n우승할 확률은\n......",
    "2:1": "99.9퍼센트!!",
    "3:0": ",\n재미있어 보이는 아이템이\n있습니다...",
    "3:1": "키 아이템을\n보시지 않겠습니까?"
  },
  "677028": {
    "1:0": "지금 돌아왔다!",
    "1:1": "역시 인터넷은\n좋아!!",
    "1:2": "마음껏 불을 뿜을 수\n있으니까!!",
    "2:0": "쳇, 당해 버렸어\n제대로 오퍼레이트\n하라고!!"
  },
  "677774": {
    "1:1": ",\n메일이야!",
    "2:1": ",\n메일이야!",
    "3:1": ",\n메일이야!",
    "4:1": "메일이야!",
    "5:1": "메일이야!",
    "6:1": "메일이야!",
    "7:1": "메일이야!",
    "20:1": "메일이야!",
    "21:1": "메일이야!",
    "22:1": "메일이야!",
    "23:1": "메일이야!",
    "24:1": "메일이야!",
    "25:1": "메일이야!",
    "26:1": "메일이야!"
  },
  "680370": {
    "1:0": "주말의\n토너먼트를 위해,",
    "1:1": "인터넷에서\n실력을 갈고닦지 않겠나?",
    "2:0": "오늘 토너먼트의,\n참가자들은 모두",
    "2:1": "나의 우레가\n얼마나 무서운지\n떨게 될 것이다...",
    "3:0": "흠...\n뭔가 재미있어 보이는\n아이템이 있군...",
    "3:1": ",\n키 아이템을\n보지 않겠나..."
  },
  "682054": {
    "10:1": ",\n임무 완료입니다",
    "10:2": "오피셜에서\n메일이 왔습니다",
    "11:1": ",\n임무 실패입니다",
    "11:2": "오피셜에서\n메일이 왔습니다",
    "12:0": ",\n남은 시간은",
    "12:1": "분입니다",
    "13:0": ",\n시간이 없습니다\n서두르시죠!!",
    "50:0": "제가 이런 실수를...\n죄송합니다\n다음에는 반드시!!",
    "51:0": ",\n수고하셨습니다",
    "51:1": "계산을 통해\n뭔가를 깨달은\n기분이 듭니다",
    "52:0": ",\n수고하셨습니다",
    "52:1": "...음?\n...문제집에서\n뭔가가...",
    "52:2": "제니가\n나왔습니다\n받아 두시죠",
    "53:0": ",\n수고하셨습니다",
    "53:1": "...음?\n...문제집에서\n뭔가가...",
    "53:2": "버그 조각이",
    "53:3": "개\n나왔습니다\n받아 두시죠",
    "60:0": "죄송합니다\n다음에는 반드시!",
    "61:0": ",\n수고하셨습니다",
    "61:1": "편지 사이에서\n뭔가가 나왔습니다\n......",
    "61:2": "「HP 메모리」입니다!\n바로 넣겠습니다",
    "62:0": ",\n수고하셨습니다",
    "62:1": "편지 사이에서\n뭔가가 나왔습니다\n......",
    "62:2": "제니입니다\n감사히 받아\n두시죠",
    "63:0": ",\n수고하셨습니다",
    "63:1": "편지 사이에서\n뭔가가 나왔습니다\n......",
    "63:2": "버그 조각",
    "63:3": "개입니다\n감사히 받아\n두시죠"
  },
  "682504": {
    "1:1": " 방송이\n시작할 시간입니다",
    "2:1": "\n일정의 시간입니다",
    "2:2": "늦으면\n상대방에게 실례입니다\n서두르시죠",
    "3:0": ",\n식사 시간입니다\n자, 식기 전에 드시죠",
    "4:0": ",\n학원으로 갈\n시간입니다",
    "4:1": "일찍 가시는 편이\n좋을 것 같습니다",
    "5:1": " 일정의\n시간입니다",
    "6:0": "그리고...",
    "21:1": " 방송이\n시작할 시간입니다",
    "22:1": "\n일정의 시간입니다",
    "22:2": "늦으면\n상대방에게 실례입니다\n서두르시죠",
    "23:0": ",\n식사 시간입니다\n자, 식기 전에 드시죠",
    "24:0": ",\n학원으로 갈\n시간입니다",
    "24:1": "일찍 가시는 편이\n좋을 것 같습니다",
    "25:1": " 일정의\n시간입니다",
    "26:0": "그리고..."
  },
  "688900": {
    "1:0": "제 계산으로는,\n슬슬",
    "3:0": "일정의 시간이에요!",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없네요",
    "11:2": " 부터\n",
    "12:0": "이네요"
  },
  "691994": {
    "1:0": "토너먼트는\n주말이다...",
    "1:1": "이 주먹을 더\n단련해야겠군...",
    "2:0": "오늘 토너먼트는,\n이 주먹으로 승리를\n거머쥔다!!",
    "3:0": "...재미있어 보이는\n아이템이 있나 보군",
    "3:1": ",\n키 아이템을\n볼까..."
  },
  "693590": {
    "1:0": "다, 다녀왔어...",
    "1:1": "나, 나, 「다녀왔어」\n라는 말, 좋아",
    "2:0": "다, 당했어...\n다, 다음엔 잘할 테니까\n나, 버리지 마..."
  },
  "693778": {
    "1:0": "플러그인!\n정크맨.EXE,\n트랜스미션!!"
  },
  "697268": {
    "1:0": "상태가 안 좋나?",
    "1:1": "오퍼레이션이\n날카롭지 못하다...",
    "2:0": ",\n상태 좋다...\n나, 알아...",
    "3:0": "이, 이기진 못했지만,\n지지도 않았으니까\n나, 슬프지 않아!"
  },
  "699194": {
    "1:1": ",\n메일이야퓨!",
    "2:1": ",\n메일이야퓨!",
    "3:1": ",\n메일이야퓨!",
    "4:1": "메일이야퓨!",
    "5:1": "메일이야퓨!",
    "6:1": "메일이야퓨!",
    "7:1": "메일이야퓨!",
    "20:1": "메일이야퓨!",
    "21:1": "메일이야퓨!",
    "22:1": "메일이야퓨!",
    "23:1": "메일이야퓨!",
    "24:1": "메일이야퓨!",
    "25:1": "메일이야퓨!",
    "26:1": "메일이야퓨!"
  },
  "65E828": {
    "1:0": "아쉬웠네...\n다음엔 힘내자!",
    "2:0": "해냈어!!\n다음에도 이 기세로\n힘내자!!",
    "3:0": "좋은 승부였어!"
  },
  "66B8B0": {
    "1:0": "푸슈...\n나는 윈드맨\n바람을 다스리는 내비다",
    "1:1": "나와 함께\n바람을 일으키지 않겠나",
    "2:0": "푸슈...\n오랜만이군",
    "2:1": "함께 새로운\n바람을 일으키지 않겠나"
  },
  "66F6A0": {
    "1:0": ",\n주말에는\n토너먼트가 있었지",
    "1:1": "시합을 위해\n수련을\n쌓도록 하자",
    "1:2": "푸슈~...",
    "2:0": "드디어 결전의 날이\n온 모양이군...",
    "2:1": ",\n마음의 준비는\n되어 있겠지!?",
    "3:0": ",\n뭔가 재미있어 보이는\n아이템이 있나 보군",
    "3:1": "키 아이템을\n보지 않겠나?"
  },
  "66FC98": {
    "1:0": "...푸슈",
    "2:0": "보았나, 풍신의 춤을!",
    "3:0": "무승부인가...",
    "3:1": "다음을 기대하지..."
  },
  "670DF4": {
    "1:0": "저는 서치맨\n당신의 파트너입니다",
    "1:1": "저의 파트너가\n되셨으니,",
    "1:2": "제 목숨은\n당신께 맡기겠습니다",
    "2:0": "오랜만입니다",
    "2:1": "함께 임무를\n수행하시죠"
  },
  "67133C": {
    "1:0": "서치맨,\n지금 돌아왔습니다",
    "1:1": "파워 차지 완료\n언제든 출격할 수 있습니다",
    "2:0": "...임무 실패\n죄송합니다"
  },
  "67593C": {
    "1:0": "방금 오퍼레이션은,\n조금 거칠었습니다",
    "1:1": "제 목숨은\n당신께 달려 있습니다",
    "1:2": "그 점을 잊지 말아\n주십시오",
    "2:0": "최근 데이터를\n통계로 분석해 보면,",
    "2:1": "다음 배틀에서 이길\n확률은...",
    "2:2": "98퍼센트!!",
    "3:0": "무승부가 될 줄은\n예상하지 못했습니다..."
  },
  "676AE4": {
    "1:0": "여어,\n나는 파이어맨\n이라고 한다",
    "1:1": "잘 부탁한다",
    "1:2": "함께 뜨겁게\n타오르자!",
    "2:0": "오랜만이잖아",
    "2:1": "응? 조금\n식어 버린 거\n아니야?",
    "2:2": "흥, 뭐 좋아\n다시 함께\n뜨거워지자"
  },
  "6770B8": {
    "70:0": "으, 으아!!",
    "70:1": "내가 이런 실수를!\n젠장, 다음에 할 때는\n반드시 복수한다!!",
    "71:0": "훗, 대충\n이 정도지!!",
    "71:1": "왠지 말이야,",
    "71:2": "힘이 부글부글\n솟아오르는 느낌이\n드는데!!",
    "72:0": "훗, 대충\n이 정도지!!",
    "72:1": "어라, 뭔가가\n전송되어 왔어",
    "72:2": "어딘가의 군대에서\n온 것 같은데...",
    "72:3": "오옷!!\n",
    "72:4": "제니가\n들어 있잖아!!",
    "72:5": "뭔지는 모르겠지만,\n이득 봤네!!",
    "73:0": "훗, 대충\n이 정도지!!",
    "73:1": "어라, 뭔가가\n전송되어 왔어",
    "73:2": "어딘가의 군대에서\n온 것 같은데...",
    "73:3": "오옷!!\n버그 조각",
    "73:4": "개가\n들어 있잖아!!",
    "73:5": "뭔지는 모르겠지만,\n이득 봤네!!"
  },
  "677C94": {
    "1:0": "카아앗!!\n불완전 연소다!",
    "1:1": "다음이다, 다음!!\n다음 토너먼트를\n위해 특훈이다!!",
    "2:0": "타, 타 버렸어...\n완전 연소다",
    "2:1": "하지만 지금 내 안에\n새롭게 생겨난\n불씨가 말이야,",
    "2:2": "어서 타오르고 싶다며\n이글거리고 있다고!",
    "10:0": ",\n참가 신청을 안 했잖아!",
    "20:0": ",\n타오르자!!",
    "21:0": ",\n타오르자!!",
    "22:0": ",\n타오르자!!",
    "23:0": ",\n타오르자!!"
  },
  "677E58": {
    "1:0": "그러고 보니 슬슬",
    "3:0": "일정의 시간 아니야?",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없어",
    "11:2": " 부터\n",
    "12:0": "라고!"
  },
  "67AD3C": {
    "1:0": "크크크...\n주말에는\n토너먼트다!!",
    "1:1": "불타오르는군...",
    "1:2": "야, 인터넷으로\n가자!!\n가만히 있을 수 없어!",
    "2:0": "드디어 토너먼트\n날이 왔군...",
    "2:1": "불타오른다!\n그리고 태워 버린다!!",
    "3:0": "야, 재미있어 보이는\n아이템이 있잖아",
    "3:1": "키 아이템을\n한번 봐!"
  },
  "67B3D0": {
    "1:0": "네 오퍼레이션은\n뜨거움이 부족해!!",
    "1:1": "더 뜨거워지라고!!",
    "2:0": "방금 그거야...\n방금 그 뜨거움이야!!\n하면 되잖아!",
    "3:0": "어중간한\n불길이군..."
  },
  "67C4CC": {
    "1:0": "나는 썬더맨\n잘 부탁한다",
    "1:1": "나와 함께 지내며",
    "1:2": "네가 긍지 높은\n인간이 되기를\n바란다",
    "2:0": "오랜만이군...",
    "2:1": "우레의 고결한\n마음을 잊지는\n않았겠지..."
  },
  "67C9FC": {
    "1:0": "...후, 지금 돌아왔다",
    "1:1": "오늘도 인터넷에\n전력이 가득하군...",
    "2:0": "이 내가 패했다고?\n...전력이\n부족한 것인가?"
  },
  "67CB24": {
    "1:0": "플러그인!\n썬더맨.EXE,\n트랜스미션!!"
  },
  "67CED8": {
    "1:1": ",\n메일이 도착했다...",
    "2:1": ",\n메일이 도착했다...",
    "3:1": ",\n메일이 도착했다...",
    "4:1": "메일이 도착했다...",
    "5:1": "메일이 도착했다...",
    "6:1": "메일이 도착했다...",
    "7:1": "메일이 도착했다...",
    "20:1": "메일이 도착했다...",
    "21:1": "메일이 도착했다...",
    "22:1": "메일이 도착했다...",
    "23:1": "메일이 도착했다...",
    "24:1": "메일이 도착했다...",
    "25:1": "메일이 도착했다...",
    "26:1": "메일이 도착했다..."
  },
  "67D44C": {
    "1:0": "서, 설마...\n우리가 패배하고\n말다니...",
    "1:1": "이 놀라움이야말로\n「청천벽력」이군",
    "2:0": "잘했다,\n",
    "2:2": "우레와도 같은\n오퍼레이션이었다",
    "10:0": ",\n참가 신청을 하지 않았군",
    "20:0": "드디어 시작이군...\n전력을 다하겠다",
    "21:0": "드디어 시작이군...\n전력을 다하겠다",
    "22:0": "드디어 시작이군...\n전력을 다하겠다",
    "23:0": "드디어 시작이군...\n전력을 다하겠다"
  },
  "67D5F8": {
    "1:0": "그러고 보니... 곧",
    "3:0": "일정의 시간이었지...",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없군...",
    "11:2": " 부터\n",
    "12:0": "다..."
  },
  "6808C4": {
    "1:0": "이 패배의 맛을,\n절대 잊지 말거라...",
    "2:0": "네 마음속에서\n격렬한 번개가\n보인다...",
    "2:1": "그런 때에는\n강한 법이다...",
    "3:0": "제대로 기세를\n타지 못했군..."
  },
  "681AB8": {
    "1:0": "처음 뵙겠습니다",
    "1:1": "저는 브루스라고\n합니다",
    "1:2": "잘 부탁드립니다",
    "2:0": "오랜만입니다",
    "2:1": ",\n다시 잘\n부탁드립니다"
  },
  "681FD4": {
    "1:0": "지금 돌아왔습니다\n",
    "1:1": ",\n수고하셨습니다",
    "2:0": "죄송합니다\n제 실수입니다...",
    "2:1": "이런 실수를\n저지르다니..."
  },
  "6824B8": {
    "1:0": "플러그인!\n브루스.EXE,\n트랜스미션!!"
  },
  "6827F8": {
    "1:1": ",\n메일입니다",
    "2:1": ",\n메일입니다",
    "3:1": ",\n메일입니다",
    "4:1": "메일입니다!",
    "5:1": "메일입니다!",
    "6:1": "메일입니다!",
    "7:1": "메일입니다!",
    "10:1": ",\n오피셜에서\n임무가 들어왔습니다",
    "20:1": "메일입니다!",
    "21:1": "메일입니다!",
    "22:1": "메일입니다!",
    "23:1": "메일입니다!",
    "24:1": "메일입니다!",
    "25:1": "메일입니다!",
    "26:1": "메일입니다!"
  },
  "682D68": {
    "1:0": ",\n죄송합니다\n......",
    "1:1": "제 힘이 부족했습니다\n하지만 다음에는\n반드시...!!",
    "2:0": "해냈군요...\n",
    "2:1": "최고의\n오퍼레이션이었습니다",
    "10:0": ",\n아쉽지만,\n참가 신청을 하지 않으셨습니다",
    "20:0": "평소 특훈의\n성과를,\n지금 보여 줄 때입니다!!",
    "21:0": "평소 특훈의\n성과를,\n지금 보여 줄 때입니다!!",
    "22:0": "평소 특훈의\n성과를,\n지금 보여 줄 때입니다!!",
    "23:0": "평소 특훈의\n성과를,\n지금 보여 줄 때입니다!!"
  },
  "682F44": {
    "3:0": "일정의 시간이\n다가오고 있습니다",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없습니다",
    "11:2": " 부터\n",
    "12:0": "입니다"
  },
  "685B7C": {
    "1:0": "이번 주말에는 드디어\n토너먼트로군요",
    "1:1": "실전에 대비해,\n기술을 갈고닦으시죠",
    "2:0": ",\n토너먼트 당일입니다",
    "2:1": "출전하는 이상\n반드시 우승\n하시죠",
    "3:0": ",\n뭔가 재미있어 보이는\n아이템이 있습니다",
    "3:1": "키 아이템을\n보시는 게\n어떻겠습니까..."
  },
  "68611C": {
    "1:0": "죄송합니다\n제 실수입니다...",
    "2:0": ",\n훌륭한 오퍼레이션\n이었습니다!",
    "3:0": "죄송합니다\n마무리가 부족했다고\n반성하고 있습니다"
  },
  "68787C": {
    "1:0": ",\n수고하셨어요",
    "1:1": "어때요, 제 움직임은\n철저히 계산된\n것이었죠?",
    "2:0": "아야야야...",
    "2:1": "이상하네요...\n제 계산으로는\n이길 수 있었는데"
  },
  "68BAAC": {
    "1:0": "아, 그러고 보니\n주말에\n토너먼트가 있네요",
    "1:1": "일단\n특훈이라도 할까요?",
    "1:2": "싫으시면\n안 하셔도 괜찮아요",
    "2:0": "토너먼트 날이\n왔네요,",
    "2:1": "뭐, 어떻게든\n될 테니까,",
    "2:2": "할 수 있는 만큼\n힘내자고요",
    "3:0": "으음! 뭔가\n재미있는 아이템이\n있나 보네요!",
    "3:1": "키 아이템을\n한번 보죠!"
  },
  "68C2CC": {
    "1:0": "제 계산에\n오류가...!?",
    "2:0": "제 계산대로\n됐네요!!",
    "3:0": "무승부가 될\n확률까지는,",
    "3:1": "계산하지\n못했어요..."
  },
  "68D3C8": {
    "1:0": "...나는 메탈맨\n...잘 부탁한다",
    "1:1": "함께 주먹을\n단련하자",
    "2:0": "오랜만이군...",
    "2:1": "많은 말은 않겠지만\n다시 한번...\n...잘 부탁한다"
  },
  "68D8F8": {
    "1:0": "...돌아왔다\n오늘 주먹의 날카로움은\n제법이었군...",
    "2:0": "...분하다!\n주먹을 더\n단련해야겠군..."
  },
  "68DD4C": {
    "1:0": "플러그인!\n메탈맨.EXE,\n트랜스미션!!"
  },
  "68DD98": {
    "1:0": " 방송이\n시작할 시간이다...",
    "1:1": "나는 TV를 그리\n좋아하지 않지만\n......",
    "2:0": "\n일정의 시간이다",
    "2:1": "「가까운 사이에도\n 예의가 필요하다」",
    "2:2": "약속에\n늦지 말거라",
    "3:0": "밥 먹을 시간이다",
    "3:1": "건강의 기본은\n식사다\n든든히 먹고 와라",
    "4:0": "학원 갈 시간이다\n열심히 하고 와라...",
    "5:1": " 일정의\n시간이다...",
    "6:0": "그리고...",
    "21:0": " 방송이\n시작할 시간이다...",
    "21:1": "나는 TV를 그리\n좋아하지 않지만\n......",
    "22:0": "\n일정의 시간이다",
    "22:1": "「가까운 사이에도\n 예의가 필요하다」",
    "22:2": "약속에\n늦지 말거라",
    "23:0": "밥 먹을 시간이다",
    "23:1": "건강의 기본은\n식사다\n든든히 먹고 와라",
    "24:0": "학원 갈 시간이다\n열심히 하고 와라...",
    "25:1": " 일정의\n시간이다...",
    "26:0": "그리고..."
  },
  "68E7BC": {
    "1:0": "...슬슬,",
    "3:0": "일정의 시간이군",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없는 모양이군...",
    "11:2": " 부터\n",
    "12:0": "군..."
  },
  "691F80": {
    "1:0": "내 주먹이\n녹슬었단 말인가...",
    "2:0": "확실한 승리를\n거두기 위해,",
    "2:1": "주먹을 더\n단련해야 한다",
    "3:0": "다음에는 확실히\n끝장을 낸다!!"
  },
  "69303C": {
    "1:0": "나, 나는 정크맨\n...",
    "1:1": "나, 누군가의 내비가\n되는 건 처음...\n조금 부끄럽다",
    "1:2": "...자, 잘 부탁한다",
    "2:0": "나, 나, 버림받은\n것이 아니었구나!!",
    "2:1": "다시 네 PET에\n들어가도 되는 거지?",
    "2:2": "다, 다행이다..."
  },
  "6941DC": {
    "1:0": "아, 생각났다...\n스, 슬슬",
    "3:0": "일정의 시간이다",
    "10:0": "오늘,\n등록된\n일정은...",
    "10:1": "아무것도 없다...",
    "11:2": " 부터\n",
    "12:0": "다..."
  },
  "696CF4": {
    "1:0": "주, 주말에는\n토너먼트가 있지...\n",
    "1:2": "하, 함께\n특훈해서,\n우승한다!",
    "2:0": "오, 오늘의\n토너먼트,",
    "2:1": "나, 열심히\n할 테니까,",
    "2:2": "도\n힘내라",
    "3:0": "재, 재미있어 보이는\n아이템 냄새가 난다",
    "3:1": "키 아이템을\n한번 보자..."
  },
  "6989B0": {
    "1:0": "퓨퓨퓨~!\n아~ 재미있었어퓨",
    "2:0": "분해퓨~~\n울 것 같아퓨~~\n다음엔 안 질 거야퓨~"
  },
  "698A2C": {
    "60:0": "퓨~...\n추, 추운 건\n싫어퓨~",
    "61:0": "퓨퓨!\n해냈어퓨!",
    "61:1": "추위를 극복하고\n승리를 거뒀어\n퓨~~!",
    "61:2": "퓨!\n편지 사이에서\n뭔가가 나왔어퓨",
    "61:3": "「HP 메모리」야퓨!\n감사히\n받을게퓨!",
    "62:0": "퓨퓨!\n해냈어퓨!",
    "62:1": "추위를 극복하고\n승리를 거뒀어\n퓨~~!",
    "62:2": "퓨!\n편지 사이에서\n뭔가가 나왔어퓨",
    "62:3": "제니야퓨!\n감사히\n받을게퓨!",
    "63:0": "퓨퓨!\n해냈어퓨!",
    "63:1": "추위를 극복하고\n승리를 거뒀어\n퓨~~!",
    "63:2": "퓨!\n편지 사이에서\n뭔가가 나왔어퓨",
    "63:3": "버그 조각",
    "63:4": "개야퓨!\n감사히\n받을게퓨!"
  },
  "698CB0": {
    "1:0": "플러그인!\n아쿠아맨.EXE,\n트랜스미션!!"
  },
  "698CFC": {
    "1:0": "퓨,",
    "1:1": "퓨,",
    "1:2": "퓨,",
    "1:3": "\n퓨~~~!",
    "1:4": " 방송이\n시작할 시간이야퓨!",
    "1:5": "함께 보자퓨!",
    "2:0": "퓨,",
    "2:1": "퓨,",
    "2:2": "퓨,",
    "2:3": "\n퓨~~~!",
    "2:4": "\n일정의 시간이야퓨",
    "2:5": "나도 데리고 가\n줬으면 좋겠어퓨~",
    "3:0": "퓨,",
    "3:1": "퓨,",
    "3:2": "퓨,",
    "3:3": "\n퓨~~~!",
    "3:4": "밥 먹을 시간이야퓨~!\n따끈따끈한 밥,\n먹자퓨~!",
    "4:0": "퓨,",
    "4:1": "퓨,",
    "4:2": "퓨,",
    "4:3": "\n퓨~~~!",
    "4:4": "학원 갈 시간이야퓨!\n힘내퓨!",
    "5:0": "퓨,",
    "5:1": "퓨,",
    "5:2": "퓨,",
    "5:3": "\n퓨~~~!",
    "5:5": " 일정의\n시간이야퓨!",
    "6:0": "음~ 그리고...",
    "21:0": "퓨,",
    "21:1": "퓨,",
    "21:2": "퓨,",
    "21:3": "\n퓨~~~!",
    "21:4": " 방송이\n시작할 시간이야퓨!",
    "21:5": "함께 보자퓨!",
    "22:0": "퓨,",
    "22:1": "퓨,",
    "22:2": "퓨,",
    "22:3": "\n퓨~~~!",
    "22:4": "\n일정의 시간이야퓨",
    "22:5": "나도 데리고 가\n줬으면 좋겠어퓨~",
    "23:0": "퓨,",
    "23:1": "퓨,",
    "23:2": "퓨,",
    "23:3": "\n퓨~~~!",
    "23:4": "밥 먹을 시간이야퓨~!\n따끈따끈한 밥,\n먹자퓨~!",
    "24:0": "퓨,",
    "24:1": "퓨,",
    "24:2": "퓨,",
    "24:3": "\n퓨~~~!",
    "24:4": "학원 갈 시간이야퓨!\n힘내퓨!",
    "25:0": "퓨,",
    "25:1": "퓨,",
    "25:2": "퓨,",
    "25:3": "\n퓨~~~!",
    "25:5": " 일정의\n시간이야퓨!",
    "26:0": "음~ 그리고..."
  },
  "6996DC": {
    "1:0": "퓨, 퓨이~~...\n져 버렸어퓨~",
    "1:1": "하지만 분하다고\n울지는 않을 거야퓨!!",
    "1:2": "눈물은 기쁠 때\n흘리려고 아껴 둘 거야퓨!!",
    "2:0": "~\n해냈어퓨~",
    "2:1": "퓨~이, 퓨~이...\n기뻐퓨~!!",
    "10:0": ",\n참가 신청을 안 했어퓨",
    "20:0": ",\n출전하는 이상 반드시\n우승할 거야퓨!",
    "21:0": ",\n출전하는 이상 반드시\n우승할 거야퓨!",
    "22:0": ",\n출전하는 이상 반드시\n우승할 거야퓨!",
    "23:0": ",\n출전하는 이상 반드시\n우승할 거야퓨!"
  },
  "6998DC": {
    "1:0": "퓨퓨! 곧,",
    "3:0": "일정의 시간이야퓨!",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없어퓨!",
    "11:2": " 부터\n",
    "12:0": "야퓨!"
  },
  "69C8FC": {
    "1:0": "토너먼트를 위해\n연습하자퓨!",
    "1:1": "열심히 하면 분명\n우승할 수 있어퓨!",
    "2:0": "퓨퓨퓨퓨...",
    "2:1": ".........\n토너먼트 날이야퓨\n기, 긴장돼퓨",
    "3:0": "퓨퓨!\n뭔가 재미있는\n아이템이 있어퓨!",
    "3:1": "키 아이템을\n한번 보자퓨!"
  },
  "69CF44": {
    "1:0": "푸퓨~...",
    "1:1": "왠지 머릿속의\n물이 줄어든 것\n같아퓨~",
    "2:0": "퓨퓨퓨~!!\n정말 상태가\n좋아퓨!!",
    "2:1": "머리에서 물이\n뿜어져 나와퓨~!!",
    "3:0": "모처럼\n배틀을 했으니까퓨,\n이기고 싶었어퓨~"
  },
  "69E088": {
    "1:0": "나는 우드맨...",
    "1:1": "말은 그다지\n잘하지 못하지만\n잘 부탁한다...",
    "1:2": "네게 대지의\n은총을...",
    "2:0": "오랜만이군...",
    "2:1": "다시 한번\n네게 대지의\n은총을..."
  },
  "69E5A8": {
    "1:0": "지금 돌아왔다...\n후, 조금 쉴까",
    "2:0": "당해 버렸군...\n치유의 힘이\n부족했던 것인가..."
  },
  "69E6BC": {
    "1:0": "플러그인!\n우드맨.EXE,\n트랜스미션!!"
  },
  "69E708": {
    "1:0": "...슬슬\n",
    "1:1": " 방송의\n시간 아니냐?",
    "2:1": "\n일정의 시간이\n된 모양이군",
    "3:0": "밥 먹을 시간이다\n나도 조금\n출출해지는군",
    "4:0": "슬슬 학원에 갈\n시간이다",
    "4:1": "지식은 중요한\n양분이다",
    "4:2": "지금 흡수해\n둬야 한다",
    "5:0": "...슬슬\n",
    "5:1": " 일정의\n시간이다...",
    "6:0": "그리고...",
    "21:0": "...슬슬\n",
    "21:1": " 방송의\n시간 아니냐?",
    "22:1": "\n일정의 시간이\n된 모양이군",
    "23:0": "밥 먹을 시간이다\n나도 조금\n출출해지는군",
    "24:0": "슬슬 학원에 갈\n시간이다",
    "24:1": "지식은 중요한\n양분이다",
    "24:2": "지금 흡수해\n둬야 한다",
    "25:0": "...슬슬\n",
    "25:1": " 일정의\n시간이다...",
    "26:0": "그리고..."
  },
  "69F11C": {
    "1:0": "...곧",
    "3:0": "일정의 시간이다",
    "10:0": "오늘 등록된\n일정은...",
    "10:1": "아무것도 없군",
    "11:2": " 부터\n",
    "12:0": "다..."
  },
  "6A207C": {
    "1:0": "주말의\n토너먼트가\n다가오는군...",
    "1:1": "만반의 준비를 하고\n시합에 나서야 한다",
    "2:0": "드디어 토너먼트\n날이 왔군...",
    "2:1": "평소 특훈의\n성과를 낼 수\n있다면,",
    "2:2": "우승을\n거머쥘 수 있을 것이다\n긴장을 풀거라",
    "3:0": ",\n재미있어 보이는\n아이템을 갖고 있군",
    "3:1": "키 아이템을\n볼까..."
  }
}
EXCLUDED={"6770B8:0:0","682054:0:0","698A2C:0:0"}
CHOICES=set()
LABELS=set()
CONTEXT={
  "672124": "Search-themed mission, trust, preparation and outcomes; source probabilities 99.9 and 98 immutable. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "675338": "Search-themed mission, trust, preparation and outcomes; source probabilities 99.9 and 98 immutable. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "677028": "Fire-themed greetings, return, minigame rewards, mail and tournament alerts. Source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "677774": "Fire-themed greetings, return, minigame rewards, mail and tournament alerts. Source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "680370": "Thunder-themed pride, lightning, return, plugin, mail, schedules and tournament outcomes. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "682054": "Proto-themed formal greeting, mission and minigame results, mail, schedules and tournament preparation. Only explicit local portraits establish portrait metadata. Arithmetic drill means workbook; source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "682504": "Proto-themed formal greeting, mission and minigame results, mail, schedules and tournament preparation. Only explicit local portraits establish portrait metadata. Arithmetic drill means workbook; source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "688900": "Number-themed calculated return, schedules and tournament outcomes; no change to previously approved 4649 greeting. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "691994": "Metal-themed fists, training, return, reminders and tournament results; explicit portraits distinct from quick alerts. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "693590": "Junk-themed timid greetings, fear of disposal, return, schedules and tournament encouragement; preserve stutter. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "693778": "Junk-themed timid greetings, fear of disposal, return, schedules and tournament encouragement; preserve stutter. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "697268": "Junk-themed timid greetings, fear of disposal, return, schedules and tournament encouragement; preserve stutter. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "699194": "Aqua-themed return, cold-letter minigame, reminders, mail and tournament encouragement; preserve separate voiced timing beats and source placeholder. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "65E828": "Battle outcome encouragement; local speaker not established. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "66B8B0": "Wind-themed greeting, tournament preparation and outcomes; wind/dance terminology remains a review candidate. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "66F6A0": "Wind-themed greeting, tournament preparation and outcomes; wind/dance terminology remains a review candidate. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "66FC98": "Wind-themed greeting, tournament preparation and outcomes; wind/dance terminology remains a review candidate. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "670DF4": "Search-themed mission, trust, preparation and outcomes; source probabilities 99.9 and 98 immutable. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "67133C": "Search-themed mission, trust, preparation and outcomes; source probabilities 99.9 and 98 immutable. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "67593C": "Search-themed mission, trust, preparation and outcomes; source probabilities 99.9 and 98 immutable. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "676AE4": "Fire-themed greetings, return, minigame rewards, mail and tournament alerts. Source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "6770B8": "Fire-themed greetings, return, minigame rewards, mail and tournament alerts. Source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "677C94": "Fire-themed greetings, return, minigame rewards, mail and tournament alerts. Source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "677E58": "Fire-themed greetings, return, minigame rewards, mail and tournament alerts. Source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "67AD3C": "Fire-themed greetings, return, minigame rewards, mail and tournament alerts. Source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "67B3D0": "Fire-themed greetings, return, minigame rewards, mail and tournament alerts. Source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "67C4CC": "Thunder-themed pride, lightning, return, plugin, mail, schedules and tournament outcomes. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "67C9FC": "Thunder-themed pride, lightning, return, plugin, mail, schedules and tournament outcomes. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "67CB24": "Thunder-themed pride, lightning, return, plugin, mail, schedules and tournament outcomes. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "67CED8": "Thunder-themed pride, lightning, return, plugin, mail, schedules and tournament outcomes. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "67D44C": "Thunder-themed pride, lightning, return, plugin, mail, schedules and tournament outcomes. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "67D5F8": "Thunder-themed pride, lightning, return, plugin, mail, schedules and tournament outcomes. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "6808C4": "Thunder-themed pride, lightning, return, plugin, mail, schedules and tournament outcomes. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "681AB8": "Proto-themed formal greeting, mission and minigame results, mail, schedules and tournament preparation. Only explicit local portraits establish portrait metadata. Arithmetic drill means workbook; source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "681FD4": "Proto-themed formal greeting, mission and minigame results, mail, schedules and tournament preparation. Only explicit local portraits establish portrait metadata. Arithmetic drill means workbook; source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "6824B8": "Proto-themed formal greeting, mission and minigame results, mail, schedules and tournament preparation. Only explicit local portraits establish portrait metadata. Arithmetic drill means workbook; source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "6827F8": "Proto-themed formal greeting, mission and minigame results, mail, schedules and tournament preparation. Only explicit local portraits establish portrait metadata. Arithmetic drill means workbook; source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "682D68": "Proto-themed formal greeting, mission and minigame results, mail, schedules and tournament preparation. Only explicit local portraits establish portrait metadata. Arithmetic drill means workbook; source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "682F44": "Proto-themed formal greeting, mission and minigame results, mail, schedules and tournament preparation. Only explicit local portraits establish portrait metadata. Arithmetic drill means workbook; source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "685B7C": "Proto-themed formal greeting, mission and minigame results, mail, schedules and tournament preparation. Only explicit local portraits establish portrait metadata. Arithmetic drill means workbook; source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "68611C": "Proto-themed formal greeting, mission and minigame results, mail, schedules and tournament preparation. Only explicit local portraits establish portrait metadata. Arithmetic drill means workbook; source placeholder remains unresolved. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "68787C": "Number-themed calculated return, schedules and tournament outcomes; no change to previously approved 4649 greeting. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "68BAAC": "Number-themed calculated return, schedules and tournament outcomes; no change to previously approved 4649 greeting. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "68C2CC": "Number-themed calculated return, schedules and tournament outcomes; no change to previously approved 4649 greeting. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "68D3C8": "Metal-themed fists, training, return, reminders and tournament results; explicit portraits distinct from quick alerts. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "68D8F8": "Metal-themed fists, training, return, reminders and tournament results; explicit portraits distinct from quick alerts. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "68DD4C": "Metal-themed fists, training, return, reminders and tournament results; explicit portraits distinct from quick alerts. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "68DD98": "Metal-themed fists, training, return, reminders and tournament results; explicit portraits distinct from quick alerts. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "68E7BC": "Metal-themed fists, training, return, reminders and tournament results; explicit portraits distinct from quick alerts. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "691F80": "Metal-themed fists, training, return, reminders and tournament results; explicit portraits distinct from quick alerts. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "69303C": "Junk-themed timid greetings, fear of disposal, return, schedules and tournament encouragement; preserve stutter. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "6941DC": "Junk-themed timid greetings, fear of disposal, return, schedules and tournament encouragement; preserve stutter. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "696CF4": "Junk-themed timid greetings, fear of disposal, return, schedules and tournament encouragement; preserve stutter. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "6989B0": "Aqua-themed return, cold-letter minigame, reminders, mail and tournament encouragement; preserve separate voiced timing beats and source placeholder. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "698A2C": "Aqua-themed return, cold-letter minigame, reminders, mail and tournament encouragement; preserve separate voiced timing beats and source placeholder. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "698CB0": "Aqua-themed return, cold-letter minigame, reminders, mail and tournament encouragement; preserve separate voiced timing beats and source placeholder. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "698CFC": "Aqua-themed return, cold-letter minigame, reminders, mail and tournament encouragement; preserve separate voiced timing beats and source placeholder. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "6996DC": "Aqua-themed return, cold-letter minigame, reminders, mail and tournament encouragement; preserve separate voiced timing beats and source placeholder. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "6998DC": "Aqua-themed return, cold-letter minigame, reminders, mail and tournament encouragement; preserve separate voiced timing beats and source placeholder. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "69C8FC": "Aqua-themed return, cold-letter minigame, reminders, mail and tournament encouragement; preserve separate voiced timing beats and source placeholder. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "69CF44": "Aqua-themed return, cold-letter minigame, reminders, mail and tournament encouragement; preserve separate voiced timing beats and source placeholder. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "69E088": "Wood-themed quiet greetings, healing, reminders, appetite, knowledge and tournament preparation. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "69E5A8": "Wood-themed quiet greetings, healing, reminders, appetite, knowledge and tournament preparation. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "69E6BC": "Wood-themed quiet greetings, healing, reminders, appetite, knowledge and tournament preparation. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "69E708": "Wood-themed quiet greetings, healing, reminders, appetite, knowledge and tournament preparation. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "69F11C": "Wood-themed quiet greetings, healing, reminders, appetite, knowledge and tournament preparation. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait.",
  "6A207C": "Wood-themed quiet greetings, healing, reminders, appetite, knowledge and tournament preparation. Native dynamic names/time/buffer inserts, jump/flag/mail/reward values, waits, box positioning, keyWait/clear and waitHold remain unchanged. Self-identification is textual context, not proof of actual runtime routing or portrait."
}
SEMANTIC_REVIEW=[
  "Exactly500 stable catalog literals across67archives, manually source-conditioned Korean drafts; not500 unique sentences. All selected sources, complete native skeletons and adjacent unselected literals inspected.",
  "Development-draft NON-DISTRIBUTION, needs_review, releasefalse. IDs/source/TPL/payload/controlcommands/numerals/brackets/newlines/leading and trailing padding immutable. No automatic prose generation, selection or shortening.",
  "Quick alerts without explicit local portrait remain speaker-unestablished. Explicit ProtoMan/MetalMan/AquaMan/WoodMan portraits in reminder scripts21..26 are recorded independently; no invented portrait inheritance or runtime routing.",
  "Dynamic names, quoted program/appointment values, hours/minutes and reward buffers require inline grammar and consumer geometry review. Source probabilities99.9/98 and native HP/item33/zenny/bugfragment/sentinel4294967295 controls unchanged.",
  "Aqua reminders retain forty separate voiced literals, including timed short sounds and following newline; thirty30-frame waits are unchanged. Mail timing/sound/flag transitions and minigame outcomes remain distinct.",
  "Unresolved source placeholders6770B8:0:0,682054:0:0,698A2C:0:0 remain in remaining denominator. Terminology, voice, meaning and actual consumer layout remain review items.",
  "Codec/font/skeleton/132px heuristic checks do not constitute human semantic or runtime approval. All remaining drafts first, then cumulative insertion/font/consumer readiness and ROM screen/save QA. No ROM/save/emulator writes."
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
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait=portrait,portrait_visibility=visibility,speaker_evidence=speaker_evidence,context=CONTEXT[archive],
            variable_context='Native dynamic inserts/branch/choice/portrait/HP commands immutable; inline grammar/geometry/reachability/runtime unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='batch500-contextual-navi-alerts',
        context=CONTEXT[archive],voice='Manual source-conditioned drafts;explicit portrait where shown;unapproved terms and voices.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Source IDs/text/TPL/payload,commands,variables,newline/padding and unselected source immutable; no ROM/save writes.',
        batch_id='batch500-044',semantic_review=SEMANTIC_REVIEW,units=units)

def main():
    if sum(v[1] for v in SOURCES.values())!=500:raise ValueError('500 batch size')
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve batch asset '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()

