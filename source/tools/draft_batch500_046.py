"""500 manually authored remaining literals; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
    "6368E8": ["a35f1a707f8ecf9e4556c31f6ef7f080afcc449fc2cec169d87ddae254c929c7",49,"translations/batch500_046_remaining_6368E8_draft_ko.json"],
    "63720C": ["e107b09a3c83cb164ceafb789c51cb0c041e9b8d3ea1edb4dcb1b47b3519c090",20,"translations/batch500_046_remaining_63720C_draft_ko.json"],
    "63746C": ["bdc73f48b7e814cde3b9fbd314c6b4529410d5ead40a69260d03a1d2cb3f2421",6,"translations/batch500_046_remaining_63746C_draft_ko.json"],
    "65AAE0": ["f2054ed89bd2014c086cff3928e93e8999ab41759253558c4c6aaaac18ee26f0",1,"translations/batch500_046_remaining_65AAE0_draft_ko.json"],
    "65CC78": ["f3fb24f845cc1cde6d8c54f6c6f6acab9a0e4e0fa71c3262a721e2299daea8ed",1,"translations/batch500_046_remaining_65CC78_draft_ko.json"],
    "662C5C": ["105f8b8e086022af68ae9d768c4bb092598d73c36ede038f5ff9ac7e5edeb994",1,"translations/batch500_046_remaining_662C5C_draft_ko.json"],
    "666430": ["8f767eed8aa11c6aabe0c218180109587f400e10274df912e04f6f4481f06676",1,"translations/batch500_046_remaining_666430_draft_ko.json"],
    "6684B0": ["5a7bb0a00eb43178c2891b62a34b281ae8f46451d822570a76389405aa5465f8",1,"translations/batch500_046_remaining_6684B0_draft_ko.json"],
    "66BE58": ["1067a454538c81a655a9dbea39a0f863b91e1cff46b2da20a81e20a0a2cea385",1,"translations/batch500_046_remaining_66BE58_draft_ko.json"],
    "66DDD0": ["a96b05f470901f3768268460d811d59fa27f2c79c70657af243aec9494819564",1,"translations/batch500_046_remaining_66DDD0_draft_ko.json"],
    "6713B8": ["59d744b9c41b39e59e8e3fefbff0a7d36bb5165ffcba4d73e582c90d0e59e450",1,"translations/batch500_046_remaining_6713B8_draft_ko.json"],
    "673770": ["f21ecd04c49931ae5cdb9649de265d86087d1a5f8784b5d3a9e8259f136fb98d",1,"translations/batch500_046_remaining_673770_draft_ko.json"],
    "6770B8": ["cd1e4921477196d4d1483472af6f755e4ca9d999e27d9401b3a72867a9a04443",1,"translations/batch500_046_remaining_6770B8_draft_ko.json"],
    "679424": ["08d5b29c0b9b61d07afecfde6c26ce71cd151b8b3a4b81cc4cf67bf12fbbab20",1,"translations/batch500_046_remaining_679424_draft_ko.json"],
    "67CA84": ["9e481e341f9ecf4d126f66cb9a4f0af168f608d85249719f628f1cec7d26e205",1,"translations/batch500_046_remaining_67CA84_draft_ko.json"],
    "67EA58": ["0cab9d610ce9fc695c8efd9d1bca15195660f9f49af99b89d0eb19804d632847",1,"translations/batch500_046_remaining_67EA58_draft_ko.json"],
    "682054": ["0b0f6938621117342b1075db31183bdf11fdaa869e91ecdfe6b14271eca8bb63",1,"translations/batch500_046_remaining_682054_draft_ko.json"],
    "6842F8": ["6b314906d2d83dc2313d0aa15c422326d5c38ca0b7335466a1f118538a25b515",1,"translations/batch500_046_remaining_6842F8_draft_ko.json"],
    "687910": ["011de5b2f54825f850e457a2a663930e9cdef89af444984dc9a66cda8de13703",2,"translations/batch500_046_remaining_687910_draft_ko.json"],
    "689DF8": ["d9ae71fed27d2e12d5fb9009d7d07e12bccf62968ec9bede66766337490bd15a",1,"translations/batch500_046_remaining_689DF8_draft_ko.json"],
    "68D96C": ["9f7debfc12475b224ed23a85f5f7607e5305b347a446fb1fe25aceff08a3e796",1,"translations/batch500_046_remaining_68D96C_draft_ko.json"],
    "68FB1C": ["35dd87100c6d957d577a414a5ffba4f668d0f86fca65b4cf56fd16d6d78bdaf9",1,"translations/batch500_046_remaining_68FB1C_draft_ko.json"],
    "69561C": ["ce59a08769a5bce43f429000a7b0a0ea9b0e1b6a2034222a8426c02ff7bc135c",1,"translations/batch500_046_remaining_69561C_draft_ko.json"],
    "698A2C": ["d5925f1c41c14a33bbe98d16985f3b6be5b45f558e6ac0e7548bc6e911940a73",1,"translations/batch500_046_remaining_698A2C_draft_ko.json"],
    "69B134": ["4d57a5b13d8a241bad0258c7aca9a4ba45904ab024cad8ad72c3e7316085478a",1,"translations/batch500_046_remaining_69B134_draft_ko.json"],
    "69E61C": ["57a4fff65ac4f191b517d8ecb71df1f7a05d717466fab65cb9ddfdd4e174463a",1,"translations/batch500_046_remaining_69E61C_draft_ko.json"],
    "6A0640": ["b996aed045bfc3d8fe20649cea2b3e19fc01f4f137efe72e2e58b145d6246cd8",1,"translations/batch500_046_remaining_6A0640_draft_ko.json"],
    "6AA730": ["24e8b82b84be1e18ce9a2557a716894a34f3898924ce8ca3e872e1245f28a735",1,"translations/batch500_046_remaining_6AA730_draft_ko.json"],
    "6ACCA8": ["3ca7c863005c80340127222a45cda2edde81bb5849cd23900fe936c1026c1995",1,"translations/batch500_046_remaining_6ACCA8_draft_ko.json"],
    "6B6050": ["8c2973728a339e9a431f286bb2af2c5a0b6a77e6181539fb45d4baaf72c149a5",1,"translations/batch500_046_remaining_6B6050_draft_ko.json"],
    "6B8478": ["ea21ba4f1b36179834c7f58e0248b8a905f795cb4fa088f5db324b12be3b800c",1,"translations/batch500_046_remaining_6B8478_draft_ko.json"],
    "6BC0C8": ["409ee8b81f35ed98f91bc22b7fc15f4fbd071a7126252dc6a6cea24a6f2866e3",1,"translations/batch500_046_remaining_6BC0C8_draft_ko.json"],
    "6BE52C": ["f955698cd253bc85e7e5947a8533c9e63818aebd8f71327ca7a4caf6ce60dd47",1,"translations/batch500_046_remaining_6BE52C_draft_ko.json"],
    "6C1BFC": ["3b07e1f3dcf178806ab53099d12b6306a2e64bccc0ceef7b6c268631d73deb79",1,"translations/batch500_046_remaining_6C1BFC_draft_ko.json"],
    "6C40AC": ["0bac9f089365be20bb9a59e2a32c73e137160db3fc409984ec3e4248de60890c",1,"translations/batch500_046_remaining_6C40AC_draft_ko.json"],
    "6C7608": ["b88d9ca903458467764e9c5525e000a9aa3e753125985a48dbd311c955c5caeb",1,"translations/batch500_046_remaining_6C7608_draft_ko.json"],
    "6C982C": ["f40535565bed9348e42ca93742f76fa253fab8753776550c9081d3e1ab3a0cef",1,"translations/batch500_046_remaining_6C982C_draft_ko.json"],
    "6CCDC0": ["39ddf05bddd8212e11412ebe77ba585b1244ca443787cf926d1b4e10a12d8c02",1,"translations/batch500_046_remaining_6CCDC0_draft_ko.json"],
    "6CF0A0": ["f0ce809263d0dbf07c144999b6da6cf0b052b69a70fc2b7c5efa5d331d32d61e",1,"translations/batch500_046_remaining_6CF0A0_draft_ko.json"],
    "6D2700": ["d4e4228d6fdff218156705377d026d1fece31cb6103e0b35b04ced676d623460",1,"translations/batch500_046_remaining_6D2700_draft_ko.json"],
    "6D44D4": ["57d96dc46c5c87191269b95757a69b0f50422d3805928f41207aed5c7f536f4c",1,"translations/batch500_046_remaining_6D44D4_draft_ko.json"],
    "6EAD18": ["3f125b6146df8c56cd896f3c96848f0818c07396db90c2f5f32d960893020918",1,"translations/batch500_046_remaining_6EAD18_draft_ko.json"],
    "701C94": ["ca7f0e88db2aae0080e5f8373907e2c19cc1f856be8e987ee0205952ce607bcf",28,"translations/batch500_046_remaining_701C94_draft_ko.json"],
    "70272C": ["341a462dc29622ed7a37d2a526d34a1bc657d9d8f450c3c93c98b9485135fb73",13,"translations/batch500_046_remaining_70272C_draft_ko.json"],
    "703080": ["13dde5626a93197d86d4de2ef86a2115a2e1126b8ecceec870b69d2626bfe953",12,"translations/batch500_046_remaining_703080_draft_ko.json"],
    "70904C": ["78297a16a2732eada21382e710c5dfaa78ac0c3abbf77b5f4c79eebb9d071873",49,"translations/batch500_046_remaining_70904C_draft_ko.json"],
    "709704": ["791f355ce72e7daed10a7b87f0d4055ad78da1ba75c9d7c1dd36bb8c6f8f87ba",13,"translations/batch500_046_remaining_709704_draft_ko.json"],
    "7097D8": ["72757c4717ad89261a351af893bf4547b93a39d28f99738088dd1a2f30c094eb",1,"translations/batch500_046_remaining_7097D8_draft_ko.json"],
    "709A34": ["e3288c56eeb45a9b98c94006b0f8cce5519dcb655120716064718644abf6073f",34,"translations/batch500_046_remaining_709A34_draft_ko.json"],
    "709D88": ["a7913cd1ec04bbde21b58f8bf9dada71f9e6f62796c75495aa4e74cd9663888d",10,"translations/batch500_046_remaining_709D88_draft_ko.json"],
    "71A37C": ["5e8ddb7c9f8c00b3cf8668451863430434386a8c1dce9c3cc8e9b64cff64de54",1,"translations/batch500_046_remaining_71A37C_draft_ko.json"],
    "71BE98": ["8f1d9bd0dc3810bac720e3a77c9582f822a42785951cb81019ac961766d760ed",1,"translations/batch500_046_remaining_71BE98_draft_ko.json"],
    "765F68": ["a72ea578f80ccd03ef4ac073f8c85b13808b69155b51eb5da2cb447396563575",1,"translations/batch500_046_remaining_765F68_draft_ko.json"],
    "765F70": ["61a5f6ea7a1afd1eb5847200f93f7ec8a49e35e6ab28dd86747063a35c9688f8",1,"translations/batch500_046_remaining_765F70_draft_ko.json"],
    "768800": ["c60f71130d41e6dc3e1c62d15966596968de7da4292e7cb5deeb36befad0e042",26,"translations/batch500_046_remaining_768800_draft_ko.json"],
    "76C918": ["7786988271e4f5c3db86997901d92ab27106a57502b67db8d0adfbc68f6625b1",1,"translations/batch500_046_remaining_76C918_draft_ko.json"],
    "76C92C": ["60edf526a6c5f1684984120f8a7cf97e95ff5e9fcd5d4565f2837734a238dec6",1,"translations/batch500_046_remaining_76C92C_draft_ko.json"],
    "7794EC": ["dfe02eb9e0e2625cdcf278aa36b99f77318d9bfa591b1657504f9f45461dfbb1",67,"translations/batch500_046_remaining_7794EC_draft_ko.json"],
    "78B588": ["0a8ad7d41b35a62d3f7092a34f07324be26ccffc884bc8ada6565ffc45baea5e",1,"translations/batch500_046_remaining_78B588_draft_ko.json"],
    "78B610": ["f3f09bced4ff1d87644f07fa1ef807723e01d4a7593b922614e6d4110538098d",1,"translations/batch500_046_remaining_78B610_draft_ko.json"],
    "78B688": ["f551adcc25b4ded04c25497ff772a15848c3d71a3bb07221e448f195c63522ea",1,"translations/batch500_046_remaining_78B688_draft_ko.json"],
    "78B784": ["8810fa5d25356f6598e2b97b71ceccc21cc63a2f1ca4af0c61e1516e36e17a6b",1,"translations/batch500_046_remaining_78B784_draft_ko.json"],
    "78B878": ["ecd3b0779fe167d5cb8e26e59d62a65fd810054f70b4ce46009c1399aef77d31",2,"translations/batch500_046_remaining_78B878_draft_ko.json"],
    "78B8F0": ["7fe0c806088ea56f79a8d825878de7be38f508261eee2e4006752d0f4e473c4e",1,"translations/batch500_046_remaining_78B8F0_draft_ko.json"],
    "78B96C": ["08fc829a2337d8badab4d995dfd73cb7da9b35001137f725e25d35e92a5ee909",2,"translations/batch500_046_remaining_78B96C_draft_ko.json"],
    "78B9E8": ["dcca6b20a2a415dba615872072b1c9df01ad36bbe60991ccdd2787e7cc621458",1,"translations/batch500_046_remaining_78B9E8_draft_ko.json"],
    "78BA60": ["1e95652ccaedc0878210c470cba6a46a9f767185f5e7611b7d008a54058e795c",1,"translations/batch500_046_remaining_78BA60_draft_ko.json"],
    "78BAE4": ["c68579d0cb1936d333097d78732f9b9da4abea94ed1bda8d82e49c3efada553e",1,"translations/batch500_046_remaining_78BAE4_draft_ko.json"],
    "78BB64": ["cdfea9dc68d1c807cb758d3ab09d8beb0673a112aa2ebc82b74e0bd96083fb1c",1,"translations/batch500_046_remaining_78BB64_draft_ko.json"],
    "78BBDC": ["85fdb8a04125c7ecfb4eb4f81f1180501e72b4580ff7331c1cba268a9cb8ebb8",1,"translations/batch500_046_remaining_78BBDC_draft_ko.json"],
    "78BC58": ["4627b714cdd1c9395515f39fded8397928b2ef14aeaf95c88176f36bec40b077",1,"translations/batch500_046_remaining_78BC58_draft_ko.json"],
    "78BCD8": ["1611a8d62045bab618f13826a02e56a73c24dcd375a4ab203c83a9f79e223030",1,"translations/batch500_046_remaining_78BCD8_draft_ko.json"],
    "78BD54": ["d21203dfff88c1fe770a2689e0924039ecd9c7a0d26b166a7d5b6ceca14cb869",1,"translations/batch500_046_remaining_78BD54_draft_ko.json"],
    "78BDC4": ["916fdeb693554d1d786a0cf23ac796a59be0f04ad43638dd333b5e511751f79b",1,"translations/batch500_046_remaining_78BDC4_draft_ko.json"],
    "78BE3C": ["6dcc43355de7b10378077bfe29cc6db8912684c6cf5cba18df2fe3f4dafb240d",1,"translations/batch500_046_remaining_78BE3C_draft_ko.json"],
    "78BEB8": ["3593b367e6b9db8bdd012c366266bbaaabcfe7daa5215d94e4342d981b35f6e7",1,"translations/batch500_046_remaining_78BEB8_draft_ko.json"],
    "79C240": ["15b2882dc2e1185f81cda0f0f541cf48c57ddce325d0ec3d93ef1e810503d654",1,"translations/batch500_046_remaining_79C240_draft_ko.json"],
    "79C8D8": ["2bb4f04f8790fbfe799c6cec869e5ee5a61db4fc63623e5597327863d71afd29",1,"translations/batch500_046_remaining_79C8D8_draft_ko.json"],
    "7ADB90": ["a90eb9e0ab586356a2d4f3246d91bbf35dbe7af3012afbf036b3e0a73c74794d",6,"translations/batch500_046_remaining_7ADB90_draft_ko.json"],
    "7ADCA4": ["4edfcc749961753494f7dad0426219acbbf3a872e7f02b3a45a104091af80d96",4,"translations/batch500_046_remaining_7ADCA4_draft_ko.json"],
    "7AE01C": ["9a7e6b38f1eb8872da09c515e9cbf79b312ab4d00c4d605b2a0a1c7838a90e8b",3,"translations/batch500_046_remaining_7AE01C_draft_ko.json"],
    "7AEEC0": ["c06c88786f3a4f936acd7bc1a4858211989787f406232debaf5f043bfea49cb7",2,"translations/batch500_046_remaining_7AEEC0_draft_ko.json"],
    "7AEF4C": ["2e371817641ed91f6674185ef9845cc9b76b190e714f794bf4332ccb152413b5",9,"translations/batch500_046_remaining_7AEF4C_draft_ko.json"],
    "7AF098": ["f0a873c3c342bf3f862f7d1b4ef7d7e4eed54a9453629c2f3931514ddb106297",4,"translations/batch500_046_remaining_7AF098_draft_ko.json"],
    "7AF2F8": ["8362e7b6141fc6158156f8b9077a15b801df52a28139ad52611704b0c8ba53f1",4,"translations/batch500_046_remaining_7AF2F8_draft_ko.json"],
    "7AF624": ["e37b45eb95836805bef795785d896378d1b26e964b5b89261e264a7021ab0bbe",4,"translations/batch500_046_remaining_7AF624_draft_ko.json"],
    "7B02AC": ["febe3a8975d8d39976b0782ca8993e868eb25f59a93ae068b3e166eae6e15d01",2,"translations/batch500_046_remaining_7B02AC_draft_ko.json"],
    "7B03C4": ["e205ac854573bef1d56f3f322d15c4f206a91270fc047e5c02920a97b81f8412",4,"translations/batch500_046_remaining_7B03C4_draft_ko.json"],
    "7B0488": ["732dc2cf0203cbc820228831c940beb13da907edf689cbc942c584fb5864978e",5,"translations/batch500_046_remaining_7B0488_draft_ko.json"],
    "7B0574": ["2136e702e868d684419e62dffddccba3d636948f2fac0f2995723bf2f7b3dba4",4,"translations/batch500_046_remaining_7B0574_draft_ko.json"],
    "7B0978": ["1d82900c6cef539ec1b216feda98082ed55bf3766fd3fccf743dff3ed84288ff",1,"translations/batch500_046_remaining_7B0978_draft_ko.json"],
    "7B19A8": ["4e0449be4ed281afd487c0239deae9442dd4b7d85cd8eb86140529cbb6355cb5",3,"translations/batch500_046_remaining_7B19A8_draft_ko.json"],
    "7B1A54": ["c22da1af6906da3bad650c0541487dd593643bbb4a57cedff954e9b18e9e6e3a",2,"translations/batch500_046_remaining_7B1A54_draft_ko.json"],
    "7B1AC4": ["5ff885c0ffc6dbfb7e3219d86ab8d5ff822b447262630a952f59a6b69c7524cb",7,"translations/batch500_046_remaining_7B1AC4_draft_ko.json"],
    "7B1BC0": ["a967c9a53c48fb511c8ffaa3c653c316c98a914b1697cb742557b296e2bda9c6",5,"translations/batch500_046_remaining_7B1BC0_draft_ko.json"],
    "7B1C78": ["b5b36d8dd44472a093e5487c5554b215cdf39213b6ef6be4999d0226472ebc64",5,"translations/batch500_046_remaining_7B1C78_draft_ko.json"],
    "7B1F44": ["1d775ee9b0f5be2ea58be2ead595bee293826ee249f864f83ab37808a34cfc8c",3,"translations/batch500_046_remaining_7B1F44_draft_ko.json"],
    "7B3120": ["0cd30721bdd6cde01580f051856f3d9ca3aac2ab2d685f32a573f76fbc10e337",1,"translations/batch500_046_remaining_7B3120_draft_ko.json"],
    "7B3C30": ["dfbbc82d0e7f26b478dde9fe8e29ae37c3cba8f85fb1ca2a552ea2db2274d34a",1,"translations/batch500_046_remaining_7B3C30_draft_ko.json"],
    "7B3E60": ["20d2c99e9679d403a9cd261e23449551b7e14acc1fc88f6ccb5c8c20f2dc9ed5",1,"translations/batch500_046_remaining_7B3E60_draft_ko.json"],
    "7B3FF0": ["2b95c59edfc66fff2b4c4d162894f8bd15d030475fe8055d8705fe13acd95b21",10,"translations/batch500_046_remaining_7B3FF0_draft_ko.json"],
    "7B4184": ["f8ea12951356b850d407154676a4f705418ec02bbb55ea2384c212ca431381cb",14,"translations/batch500_046_remaining_7B4184_draft_ko.json"],
}
DRAFT={
  "666430": {
    "0:0": "임시 문구입니다"
  },
  "673770": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "679424": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "682054": {
    "0:0": "임시 문구입니다"
  },
  "687910": {
    "0:0": "임시 문구입니다",
    "12:0": "오류!"
  },
  "703080": {
    "0:0": " NO NAME  환·영·한·다     ",
    "1:0": " NO NAME  이봐 이봐 이봐       ",
    "2:0": " NO NAME  RE:이봐 이봐 이봐     ",
    "3:0": " NO NAME  이유          ",
    "4:0": " NO NAME  관         ",
    "5:0": " NO NAME  들어라! 내 말을!   ",
    "7:0": " NO NAME  설마 그···    ",
    "8:0": " NO NAME  수집가        ",
    "9:0": " NO NAME  언더 세계는 하극상 ",
    "10:0": " NO NAME  신입에게 세례를 ",
    "11:0": " NO NAME  어둠의 힘은 사라지지 않는다 ",
    "12:0": " NO NAME  끝없는 세계    "
  },
  "709704": {
    "0:0": "개인용 휴대 단말기\n록맨은 이 PET에\n설치되어 있다",
    "33:0": "HP 메모리",
    "34:0": "확장 메모리",
    "35:0": "레귤러UP1",
    "36:0": "레귤러UP2",
    "37:0": "레귤러UP3",
    "38:0": "서브 메모리",
    "39:0": "미니 에너지",
    "40:0": "풀 에너지",
    "41:0": "시노비 대시",
    "42:0": "언트랩",
    "43:0": "에너미 서치",
    "44:0": "오픈 록"
  },
  "768800": {
    "0:0": "우선 소울 유니존을 하려면\n소울에 맞는 칩1장을\n제물로 바쳐야 한다",
    "1:0": "제물?\n그럼 버린다는 거야?",
    "2:0": "그렇다, 지금 록맨이\n유니존할 수 있는 소울은\n거츠 소울이지",
    "2:1": "거츠맨은 그 주먹으로\n패널까지 부숴 버리는\n강력한 소울···",
    "2:2": "즉 「크랙아웃」 같은\n지형 파괴 칩을\n제물로 바치면 유니존할 수 있다",
    "2:3": "방법은 이렇다,\n먼저 「크랙아웃」을\n선택하고···",
    "3:0": "다음은 이것, 유니존 명령을\n선택하는 거다",
    "4:0": "해 봐라, 넷토",
    "5:0": "지금은 연습이니\n「크랙아웃」을 선택해 봐라",
    "6:0": "넷토, 지금은 「크랙아웃」을\n선택하자, 자, 취소하고\n다시 선택해라",
    "7:0": "넷토, 유니존 명령을\n잊었구나",
    "8:0": "넷토,\n취소할 필요는 없다",
    "9:0": "지금은 도망칠 필요 없다\n자, 계속하자",
    "10:0": "봐라, 이렇게\n융합하면\n유니존 칩이 완성된다",
    "10:1": "이 상태에서 OK를 선택하면\n자동으로 소울 유니존이\n발동한다!",
    "10:2": "거츠 소울 상태에서는\n무속성과 지형 파괴 계열\n칩의 공격력이+30 증가한다",
    "10:3": "또한 B버튼 차지 샷이\n거츠 펀치로 바뀌며",
    "10:4": "B버튼을 연타하면\n무적 상태로 발사하는\n거츠 머신건을 쓸 수 있다!",
    "10:5": "실제로 써 봐라",
    "11:0": "이것이 소울 유니존이다\n잘 활용하면 상당한\n전력 UP이 된다",
    "11:1": "다만 제한 없이 얼마든지\n유니존할 수 있는 건 아니다\n몇 가지 제한이 있지",
    "11:2": "첫 번째,\n레귤러 칩은 제물로\n바칠 수 없다",
    "11:3": "두 번째,\n한 배틀에서 같은 소울로는\n한 번만 유니존할 수 있다",
    "11:4": "세 번째,\n소울 유니존을 유지할 수 있는 건\n3턴 동안뿐이다",
    "11:5": "이 제한들을 염두에 두고\n잘 생각해서 활용해라!",
    "12:0": "지금은 취소하지 않아도 된다"
  },
  "6368E8": {
    "4:0": "ABCDEFGHIJKLMNOPQRSTUVWXYZ    1234567890     !?&♯$+-×÷=¥%()/.·:’~          ",
    "20:0": "오빠·형 이름은?",
    "22:0": "언니·누나 이름은?",
    "61:0": "기타     ",
    "69:0": ": 약속",
    "70:0": "내비 데이터 칩 접수 중",
    "81:0": "[z]개 승리            0123456789      ",
    "112:0": "일",
    "113:0": "월",
    "114:0": "화",
    "115:0": "수",
    "116:0": "목",
    "117:0": "금",
    "118:0": "토",
    "130:0": "설날",
    "131:0": "세쓰분",
    "132:0": "밸런타인데이",
    "133:0": "히나마쓰리",
    "134:0": "어린이날",
    "135:0": "칠석",
    "136:0": "크리스마스이브",
    "137:0": "크리스마스",
    "138:0": "섣달그믐",
    "140:0": "!회사",
    "141:0": "!오빠·형",
    "142:0": "!남동생",
    "143:0": "!언니·누나",
    "144:0": "!여동생",
    "145:0": "!친구",
    "146:0": "!좋아하는 음식",
    "147:0": "!취미",
    "148:0": "!꿈",
    "149:0": "!좋아하는 사람",
    "150:0": "!존경하는 사람",
    "151:0": "!싫어하는 사람",
    "152:0": "!좋아하는 TV",
    "153:0": "!체육",
    "154:0": "!국어",
    "155:0": "!갖고 싶은 것",
    "156:0": "!최다 배틀",
    "157:0": "!열세 상대",
    "158:0": "!열세 C",
    "159:0": "!우세 상대",
    "160:0": "!우세 C",
    "161:0": "!주력 S1",
    "162:0": "!주력 S2",
    "163:0": "!주력 S3",
    "164:0": "!주력 M",
    "165:0": "!주력 G"
  },
  "63720C": {
    "0:0": "군",
    "1:0": "양",
    "2:0": "군",
    "3:0": "양",
    "4:0": "님",
    "5:0": "양",
    "8:0": "님",
    "9:0": "님",
    "14:0": "님",
    "15:0": "님",
    "16:0": "님",
    "17:0": "님",
    "22:0": "군",
    "23:0": "양",
    "32:0": "공",
    "33:0": "공",
    "34:0": "공",
    "35:0": "님",
    "38:0": "군",
    "39:0": "양"
  },
  "63746C": {
    "0:0": "서브 칩 데이터를\n내비에게 전송합니다",
    "1:0": "데이터 라이브러리를\n확인합니다",
    "2:0": "내비의 장비를\n설정합니다",
    "3:0": "메일을\n확인합니다",
    "4:0": "키 아이템을\n확인합니다",
    "5:0": "지금까지의 내용을\n저장합니다"
  },
  "65AAE0": {
    "0:0": "임시 문구입니다"
  },
  "65CC78": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "662C5C": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6684B0": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "66BE58": {
    "0:0": "임시 문구입니다"
  },
  "66DDD0": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6713B8": {
    "0:0": "임시 문구입니다"
  },
  "6770B8": {
    "0:0": "임시 문구입니다"
  },
  "67CA84": {
    "0:0": "임시 문구입니다"
  },
  "67EA58": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6842F8": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "689DF8": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "68D96C": {
    "0:0": "임시 문구입니다"
  },
  "68FB1C": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "69561C": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "698A2C": {
    "0:0": "임시 문구입니다"
  },
  "69B134": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "69E61C": {
    "0:0": "임시 문구입니다"
  },
  "6A0640": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6AA730": {
    "0:0": "임시 문구입니다"
  },
  "6ACCA8": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6B6050": {
    "0:0": "임시 문구입니다"
  },
  "6B8478": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6BC0C8": {
    "0:0": "임시 문구입니다"
  },
  "6BE52C": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6C1BFC": {
    "0:0": "임시 문구입니다"
  },
  "6C40AC": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6C7608": {
    "0:0": "임시 문구입니다"
  },
  "6C982C": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6CCDC0": {
    "0:0": "임시 문구입니다"
  },
  "6CF0A0": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6D2700": {
    "0:0": "임시 문구입니다"
  },
  "6D44D4": {
    "0:0": "오류!\n보고용 시트에\n기록해 주세요"
  },
  "6EAD18": {
    "10:0": " 에게"
  },
  "701C94": {
    "0:0": " 아나       인사          ",
    "1:0": " 로리에K     참가 시험        ",
    "2:0": " 노부히게     RE:참가 시험    ",
    "3:0": " 사루요시     RE:참가 시험    ",
    "4:0": " 모치미치     평일을 보내는 법    ",
    "5:0": " 로빈슨      RE:평일을 보내는 법",
    "6:0": " 츄니자와     불타는 화요일     ",
    "7:0": " 츄니자와     그리고····      ",
    "8:0": " ID08         미정       ",
    "9:0": " ID09         미정       ",
    "10:0": " ID0A          미정      ",
    "11:0": " ID0B          미정      ",
    "12:0": " ID0C          미정     ",
    "13:0": " ID0D           미정     ",
    "14:0": " ID0E          미정    ",
    "15:0": " 혼DA       흉흉하네      ",
    "16:0": " 타키타케     RE:흉흉하네    ",
    "17:0": " 우츠킨      폭주 내비      ",
    "18:0": " 울프       다음 토너먼트    ",
    "19:0": " 켄고       RE:다음 토너먼트  ",
    "20:0": " 텟신       처음 뵙겠습니다! ",
    "21:0": " 텟신       왜?          ",
    "22:0": " 유키       RE:왜?       ",
    "23:0": " 텟신       감사합니다!       ",
    "24:0": " 우츠킨      알짜 정보    ",
    "25:0": " 막키       알짜 정보 그2",
    "26:0": " 코헤이      웃으려면 웃어라!   ",
    "27:0": " 코에츠 형님   알짜 정보 그3"
  },
  "70272C": {
    "0:0": " 이나리      기분 전환 어때요?   ",
    "1:0": " VOLK     RE:기분 전환 어때요? ",
    "2:0": " 나베얀      RE:기분 전환 어때요? ",
    "3:0": " 루타       RE:기분 전환 어때요? ",
    "4:0": " 유        내 경우        ",
    "5:0": " 아야       곤란해      ",
    "6:0": " 졸리       RE:곤란해      ",
    "7:0": " 신신       한 번 더       ",
    "8:0": " 무사C      강함을 추구하는 자여!  ",
    "9:0": " 나베얀      RE:강함을 추구하는 자여",
    "10:0": " 하나       다크로이드       ",
    "11:0": " 신신       RE:다크로이드    ",
    "12:0": " 벨츠 씨     RE:다크로이드    "
  },
  "70904C": {
    "0:1": "」의\n효과가 끝났다!!",
    "1:1": "」의\n효과가 끝났다!!",
    "2:0": "개",
    "10:0": "넷토,\n메일이 도착했어!",
    "24:0": "성별을 선택해 주세요   남자 여자",
    "25:0": "나이를 입력해 주세요0123456789세",
    "26:0": "직업을 선택해 주세요유치원생초등학생중학생고등학생대학생재수생프리터회사원자영업자주부",
    "27:0": "날짜와 시각을 입력해 주세요이대로 하시겠습니까?예아니요",
    "30:0": "성별을 선택해 주세요",
    "31:0": "남자",
    "32:0": "여자",
    "33:0": "나이를 입력해 주세요",
    "34:0": "세",
    "50:0": "직업을 선택해 주세요",
    "51:0": "유치원생",
    "52:0": "재수생",
    "53:0": "초등학생",
    "54:0": "프리터",
    "55:0": "중학생",
    "56:0": "회사원",
    "57:0": "고등학생",
    "58:0": "자영업자",
    "59:0": "대학생",
    "60:0": "주부",
    "61:0": "날짜와 시각을 입력해 주세요",
    "62:0": "예",
    "73:0": "이대로 하시겠습니까?",
    "74:0": "아니요",
    "79:0": "(일)",
    "80:0": "(월)",
    "81:0": "(화)",
    "82:0": "(수)",
    "83:0": "(목)",
    "84:0": "(금)",
    "85:0": "(토)",
    "88:0": "이대로 하시겠습니까?",
    "100:0": "이름    :",
    "101:0": "성별   :",
    "102:0": "나이   :",
    "103:0": "직업 :",
    "104:0": "예",
    "105:0": "아니요",
    "106:0": "남자",
    "107:0": "여자",
    "108:0": "세",
    "110:0": "선택할 내비: ",
    "110:1": ".\n이대로 정할까요?\n",
    "110:3": "예  ",
    "110:4": "아니요"
  },
  "7097D8": {
    "0:0": "x가짜 메시지입니다"
  },
  "709A34": {
    "0:0": "다크라인  \n버그체인  \n포르테    ",
    "1:0": "다크라인   \n버그체인   \n포르테어나더 ",
    "5:0": "히트샷  \n히트브이    \n히트사이드   ",
    "10:0": "버블샷  \n버블브이  \n버블사이드  ",
    "15:0": "어택+10\n캐논  \n캐논  ",
    "20:0": "어택+10\n하이캐논  \n하이캐논  ",
    "25:0": "어택+10\n메가캐논  \n메가캐논  ",
    "30:0": "와이드소드   \n와이드블레이드  \n와이드샷1 ",
    "35:0": "와이드소드   \n와이드블레이드  \n와이드샷2 ",
    "40:0": "와이드소드   \n와이드블레이드  \n와이드샷3 ",
    "45:0": "히트브레스   \n히트브레스   \n플레임라인1 ",
    "50:0": "히트브레스   \n히트브레스   \n플레임라인2 ",
    "55:0": "히트브레스   \n히트브레스   \n플레임라인3 ",
    "60:0": "화이트웹1\n화이트웹1\n부메랑1  ",
    "65:0": "화이트웹2\n화이트웹2\n부메랑2  ",
    "70:0": "화이트웹3\n화이트웹3\n부메랑3  ",
    "75:0": "발칸1    발칸1    트윈팽1 ",
    "80:0": "발칸2    발칸2    트윈팽2 ",
    "85:0": "발칸3    발칸3    트윈팽3 ",
    "90:0": "에어하키1  \n에어하키1  \n호우간     ",
    "95:0": "에어하키2  \n에어하키2  \n호우간     ",
    "100:0": "에어하키3  \n에어하키3  \n호우간     ",
    "105:0": "일렉쇼크 \n일렉쇼크 \n마그볼트1  ",
    "110:0": "일렉쇼크 \n일렉쇼크 \n마그볼트2  ",
    "115:0": "일렉쇼크 \n일렉쇼크 \n마그볼트3  ",
    "120:0": "소드     \n와이드소드  \n롱소드  ",
    "121:0": "소드      \n와이드블레이드  \n롱블레이드  ",
    "125:0": "건델솔1  \n건델솔2  \n건델솔3  ",
    "130:0": "미니봄    \n보이즈봄1 \n카운트봄  ",
    "131:0": "미니봄    \n보이즈봄2 \n카운트봄  ",
    "132:0": "미니봄    \n보이즈봄3 \n카운트봄  ",
    "135:0": "다크홀   \n다크라인   \n포이즌아누비스 ",
    "140:0": "카와리미     \n내비스카우트   \n무라마사블레이드 ",
    "145:0": "에너지봄   \n메가에너지봄 \n스프레드건  "
  },
  "709D88": {
    "0:0": "넷토\n오늘은 뭘 할까?",
    "10:0": "요즘은 따뜻하네요",
    "11:0": "어느 날의 일정을\n입력할까요?",
    "12:0": "무엇을 등록할까요?\n",
    "12:1": "저장한 곳부터\n",
    "12:2": "데이터를 이어받아",
    "12:3": "회차 시작",
    "14:0": "저장한 곳부터\n",
    "14:1": "데이터를 이어받아",
    "14:2": "회차 시작"
  },
  "71A37C": {
    "2:0": "0123456789개[z]"
  },
  "71BE98": {
    "2:0": "캐논와이드소드히트브이에너지봄HI롱소드네오배리어블"
  },
  "765F68": {
    "0:0": "듀오"
  },
  "765F70": {
    "0:0": "그랑프리 파워"
  },
  "76C918": {
    "0:0": "듀오"
  },
  "76C92C": {
    "0:0": "그랑프리 파워"
  },
  "7794EC": {
    "0:0": "수험표 획득",
    "1:0": "견습 라이선스 획득",
    "2:0": "시민 라이선스 획득",
    "3:0": "배틀러 라이선스 획득",
    "4:0": "트로피 획득",
    "5:0": "커트 키 획득",
    "6:0": "열매 획득",
    "7:0": "뇌신상 획득",
    "8:0": "통행증 획득",
    "9:0": "커트 키2 획득",
    "10:0": "플러스 키 획득",
    "11:0": "마이너스 키 획득",
    "12:0": "합격 데이터A 획득",
    "13:0": "합격 데이터B 획득",
    "14:0": "합격 데이터C 획득",
    "15:0": "번역 도구 획득",
    "16:0": "계산 문제집 획득",
    "17:0": "얼음 편지 획득",
    "18:0": "저격 훈련 획득",
    "19:0": "실버 티켓 획득",
    "20:0": "골드 티켓 획득",
    "181:0": "빅해머 획득!",
    "182:0": "빅해머가 없어졌다!",
    "200:0": "의 등록 대회:\n",
    "200:1": "에\n등록했습니다",
    "200:2": "의 등록 대회:\n",
    "200:3": "에\n등록했습니다",
    "200:4": "의 등록 대회:\n",
    "200:5": "에\n등록했습니다",
    "200:6": "의 등록 대회:\n",
    "200:7": "에\n등록했습니다",
    "200:8": "의 등록 대회:\n",
    "200:9": "에\n등록했습니다",
    "201:0": "등록 내역이1개도\n없습니다",
    "202:0": "이상입니다",
    "220:0": "전원, 오피셜 토너먼트\n등록!",
    "221:0": "전원, 골드 토너먼트\n등록!",
    "222:0": "전원, 실버 토너먼트\n등록!",
    "223:0": "전원, 언더 토너먼트\n등록!",
    "229:0": "메일 수신",
    "230:0": "사용자 홈페이지 바닥\n타입A",
    "231:0": "사용자 홈페이지 바닥\n타입B",
    "232:0": "사용자 홈페이지 바닥\n타입C",
    "233:0": "사용자 홈페이지 바닥\n타입D",
    "234:0": "사용자 홈페이지 바닥\n타입E",
    "235:0": "사용자 홈페이지 바닥\n타입F",
    "236:0": "사용자 홈페이지 BG\n타입A",
    "237:0": "사용자 홈페이지 BG\n타입B",
    "238:0": "사용자 홈페이지 BG\n타입C",
    "239:0": "사용자 홈페이지 BG\n타입D",
    "240:0": "사용자 홈페이지 BG\n타입E",
    "241:0": "사용자 홈페이지 BG\n타입F",
    "243:0": "PA 획득",
    "244:0": "HP 메모리 획득",
    "245:0": "메일 ON",
    "246:0": "실버T 참가 OK\n골드T 참가 OK\n오피셜T 참가 OK",
    "246:1": "언더T도 참가 OK",
    "246:2": "실버는 STA002\n골드는 STA103\n오피셜은 STA203",
    "246:3": "언더는 STA303",
    "247:0": "셰이드맨 격파 플래그",
    "248:0": "100제니 획득!",
    "249:0": "10제니 획득!",
    "250:0": "키 아이템 획득!",
    "251:0": "칩 세트",
    "252:0": "대부호",
    "253:0": "서브 아이템 GET",
    "254:0": "모든 칩 획득"
  },
  "78B588": {
    "0:0": "검은 힘으로 가득 차 있는 듯한\n지역이네···\n조심해서 나아가자"
  },
  "78B610": {
    "0:0": "위험한 냄새가\n풀풀 나는 지역이거스!\n신중히 나아가거스!"
  },
  "78B688": {
    "0:0": "독기가 가득하군\n···방심하지 마라"
  },
  "78B784": {
    "0:0": "어둠의 힘이 넘쳐흐르는군\n무시무시한 곳에\n와 버렸어···"
  },
  "78B878": {
    "0:0": "엄청난 어둠의 힘입니다···\n",
    "0:1": ",\n조심하십시오···"
  },
  "78B8F0": {
    "0:0": ",\n이, 이 지역은 위험해요\n어서 나가요···"
  },
  "78B96C": {
    "0:0": "···",
    "0:1": ",\n방심하지 마라···이 지역을\n언더와 같다고 생각하지 마라···"
  },
  "78B9E8": {
    "0:0": "여, 여기는 무척\n무서운 지역이야\n그, 그런 느낌이 들어···"
  },
  "78BA60": {
    "0:0": "이 지역은 왠지\n정말 무서운 느낌이야퓨\n도, 돌아가고 싶어퓨우···"
  },
  "78BAE4": {
    "0:0": "여기는 햇빛조차 닿지 않는\n어둠의 세계인가···\n신중하게 나아간다···"
  },
  "78BB64": {
    "0:0": "별빛도 없는 어둠의 세계야\n이거 꽤 위험할지도···"
  },
  "78BBDC": {
    "0:0": "심상치 않은 힘이 느껴진다\n···끝없는 어둠이군\n긴장을 늦추지 마라···"
  },
  "78BC58": {
    "0:0": "뭔가 무시무시한\n기척이 느껴지지만,\n겁먹어서는 안 됩니다!"
  },
  "78BCD8": {
    "0:0": "이 지역에 넘쳐흐르는\n어둠의 힘···\n이거 좀 위험한데"
  },
  "78BD54": {
    "0:0": "이 지역은 무서워요···\n플러그아웃···하고 싶어요"
  },
  "78BDC4": {
    "0:0": "···어둠의 힘이\n가득한\n엄청난 지역이군···"
  },
  "78BE3C": {
    "0:0": "새까만 어둠에\n뒤덮인 지역···\n꽤 위험한 분위기네"
  },
  "78BEB8": {
    "0:0": "···훗\n조금은 즐길 수 있을 만한\n지역이군···"
  },
  "79C240": {
    "1:0": "버그조각 트레이더(임시)"
  },
  "79C8D8": {
    "0:0": "SP 트레이더(임시)"
  },
  "7ADB90": {
    "0:0": "오늘은 물속성\n바이러스가 득실거리네",
    "0:1": "물벼락을 맞지 않게\n조심해야겠어···",
    "1:0": "그쪽 칩 상점들은\n수요일엔 레이디스 데이라느니\n뭐라느니 하면서",
    "1:1": "칩을 싸게\n팔지만 말이야,",
    "1:2": "거기 버그조각\n교환소는",
    "1:3": "그런 가벼운\n행사는 전혀 하지 않는\n우직한 가게야···"
  },
  "7ADCA4": {
    "0:0": "그러고 보니 금요일은\n인터넷12에서\n배틀 모임을 하는 날이야···",
    "0:1": "이번엔 전승을\n노리겠어!!",
    "1:0": "역시 한 주의\n즐거움이라면,",
    "1:1": "금요일 배틀 모임과\n주말 토너먼트지"
  },
  "7AE01C": {
    "0:0": "청소 청소!",
    "0:1": "저는 이 지역의\n청소 담당\n프로그램입니다!",
    "0:2": "열심히 청소하고 있습니다!"
  },
  "7AEEC0": {
    "0:0": "순찰~, 순찰~\n즐겁다~!",
    "1:0": "역시 조용한 환경에서는\n공부가 잘되네!"
  },
  "7AEF4C": {
    "0:0": "으~···\n한 주가 시작되네···\n힘들어···",
    "1:0": "내 오퍼레이터는\n미용사라서\n오늘 쉬어",
    "1:1": "친구들과 쉬는 날이 안 맞아서\n조금 외로워",
    "10:0": "그러므로···\n···이렇게 되는 것이다",
    "10:1": "즉 여기에3을 더하면\n5가 되는 거지",
    "11:0": "음음···그렇구나!",
    "12:0": "Zzzzzzz···",
    "13:0": "저기, 공부하는 데\n방해하지 마!",
    "14:0": "아아아아아아아!\n전혀 모르겠어어!"
  },
  "7AF098": {
    "0:0": "두리번, 두리번···",
    "0:1": "흉악범은\n없는 것 같군···",
    "0:2": "이 근처는 언더와 가까우니\n특히 순찰에 힘을\n써야겠어···",
    "1:0": "이 지역에는 학원도 있으니\n치안을 확실하게\n지켜야 한다"
  },
  "7AF2F8": {
    "0:0": "오늘은 이 지역을\n담당하는 오피셜 내비들의\n회의 날이야",
    "1:0": "최근의 인터넷 범죄를\n억제하려면\n어떻게 해야 할까요···",
    "2:0": "역시 인터넷의 익명성이\n문제로군···",
    "2:1": "하지만 그건 각자의 도덕심에\n맡길 수밖에 없겠지···"
  },
  "7AF624": {
    "0:0": "수운차알!\n수운차알!",
    "0:1": "너도 나도\n수운차알!!",
    "1:0": "나는 말이야, 혼자\n공부하는 걸\n좋아해",
    "1:1": "주말엔 이렇게\n혼자 공부하지"
  },
  "7B02AC": {
    "0:0": "으~, 오랜만의 휴일이다!",
    "0:1": "오늘은 마음껏\n느긋하게 쉴 거야!!"
  },
  "7B03C4": {
    "0:0": "오늘은 불속성\n바이러스가 많아서인지\n유난히 덥네···",
    "1:0": "안녕, 잘 지내나!?\n나는 잘 지낸다!!",
    "1:1": "오피셜은 언제나\n기운이 넘친다!!",
    "1:2": "다아아아아아아아아앗!!"
  },
  "7B0488": {
    "0:0": "오늘은 레이디스 데이!",
    "0:1": "뭘 살까!\n역시 쇼핑은\n돈을 써야 제맛이지!",
    "0:2": "버그조각 교환소에선\n쇼핑한 느낌이 안 나!",
    "1:0": "아~, 좀 후텁지근하네!\n유난히 습도가 높지 않아?",
    "1:1": "물속성\n바이러스 때문인가?"
  },
  "7B0574": {
    "0:0": "오늘은 나무속성\n바이러스가 많은 날입니다!",
    "0:1": "나무속성 바이러스는\n잘 타니까\n화재를 조심하세요!!",
    "1:0": "나무속성 바이러스를\n이용해서",
    "1:1": "공기를 깨끗하게 만드는\n시스템을 만들 수 없을까?"
  },
  "7B0978": {
    "0:0": "언젠가 오피셜의\n눈을 피해\n언더에 가 보고 싶어···"
  },
  "7B19A8": {
    "0:0": "가끔 언더 인터넷에\n관심을 가진 젊은 내비들이",
    "0:1": "사람이 없을 때\n찾아오곤 하는데,",
    "0:2": "그런 걸 젊은 혈기에 저지르는\n무모한 짓이라고 하지···"
  },
  "7B1A54": {
    "0:0": "자, 한 주의\n시작이다",
    "0:1": "힘내자!!"
  },
  "7B1AC4": {
    "0:0": "순찰 중이야",
    "0:1": "너는 요일에 맞는\n칩을 제대로 고르고 있나?",
    "0:2": "인터넷에는 다양한\n바이러스가 나오니까",
    "1:0": "A지점, 이상 없음!!",
    "2:0": "캬~!!",
    "2:1": "역시 오피셜은\n멋있어!!",
    "2:2": "나도 언젠가는\n오피셜 넷배틀러가\n되고 싶어!!"
  },
  "7B1BC0": {
    "0:0": "오늘은 레이디스\n순찰 데이야",
    "0:1": "나, 이래 봬도\n오피셜이라고!!",
    "0:2": "대단하지?\n에헴!!",
    "1:0": "B지점, 이상 없습니다!",
    "1:1": "오늘도 평화롭습니다!!"
  },
  "7B1C78": {
    "0:0": "오피셜이 되려면···?",
    "0:1": "그, 그래···\n일단 열심히\n공부하게",
    "0:2": "알겠습니다아!!",
    "1:0": "어떻게 하면 오피셜이\n될 수 있나요!?",
    "1:1": "고, 곤란하군···"
  },
  "7B1F44": {
    "0:0": "오피셜에게는 주말 같은 건\n상관없어",
    "0:1": "항상 범죄가 발생하지 않도록\n신경을 쓰고 있지",
    "1:0": "역시 오피셜은\n최고로 멋있어!!"
  },
  "7B3120": {
    "0:0": "전뇌 세계,\n인터넷에 오신 걸 환영합니다!\n여기는 아키하라 에리어예용"
  },
  "7B3C30": {
    "0:0": "여기엔 예전에\n상점이 있었는데\n망해 버린 모양이군···"
  },
  "7B3E60": {
    "0:0": "전뇌 세계,\n인터넷에 오신 걸 환영합니다!\n여기는 아키하라 에리어예용"
  },
  "7B3FF0": {
    "0:0": "할 말은 없다···\n나와 싸워라···",
    "0:1": "덤벼!  ",
    "0:2": "싫어",
    "0:3": "겁먹었나···",
    "0:4": "아니, 그 정도 놈이라면\n싸울 가치도 없다!!",
    "1:0": "배틀 오퍼레이션, 세트!\n인!!",
    "2:0": "생각했던 것보다···\n강하군···",
    "3:0": "이 정도인가···",
    "3:1": "목숨이 아깝다면\n어서 언더에서 나가라",
    "3:2": "그 정도 실력으로는\n언더에서 통하지 않는다"
  },
  "7B4184": {
    "0:0": "누구냐···\n삭제당하러 왔느냐?",
    "0:1": "그 반대야!  ",
    "0:2": "아니야!",
    "0:3": "내 심기를\n건드리기 전에 사라져라···",
    "1:0": "네, 네놈···\n이 빚은···반드시 갚겠다",
    "2:0": "너 따위는 마무리할\n가치도 없다···사라져라",
    "3:0": "삼도천을 건널\n각오는 되었느냐···",
    "3:1": "자, 정정당당하게···\n승부!!",
    "4:0": "무슨 속셈이냐···",
    "4:1": "그 정도 인술로\n내 앞에 서다니,\n어지간히 삭제당하고 싶은가 보군",
    "4:2": "각오는 되었느냐?",
    "4:3": "물론!  ",
    "4:4": "미안!",
    "4:5": "이곳에서 꺼져라!"
  }
}
EXCLUDED={'6368E8:2:0','6368E8:3:0'}
CHOICES=set(["70904C:110:3","70904C:110:4","709D88:12:1","709D88:12:2","709D88:12:3","709D88:14:0","709D88:14:1","709D88:14:2","7B3FF0:0:1","7B3FF0:0:2","7B4184:0:1","7B4184:0:2","7B4184:4:3","7B4184:4:4"])
LABELS=set(["6368E8:4:0","6368E8:20:0","6368E8:22:0","6368E8:61:0","6368E8:69:0","6368E8:70:0","6368E8:81:0","6368E8:112:0","6368E8:113:0","6368E8:114:0","6368E8:115:0","6368E8:116:0","6368E8:117:0","6368E8:118:0","6368E8:130:0","6368E8:131:0","6368E8:132:0","6368E8:133:0","6368E8:134:0","6368E8:135:0","6368E8:136:0","6368E8:137:0","6368E8:138:0","6368E8:140:0","6368E8:141:0","6368E8:142:0","6368E8:143:0","6368E8:144:0","6368E8:145:0","6368E8:146:0","6368E8:147:0","6368E8:148:0","6368E8:149:0","6368E8:150:0","6368E8:151:0","6368E8:152:0","6368E8:153:0","6368E8:154:0","6368E8:155:0","6368E8:156:0","6368E8:157:0","6368E8:158:0","6368E8:159:0","6368E8:160:0","6368E8:161:0","6368E8:162:0","6368E8:163:0","6368E8:164:0","6368E8:165:0","63720C:0:0","63720C:1:0","63720C:2:0","63720C:3:0","63720C:4:0","63720C:5:0","63720C:8:0","63720C:9:0","63720C:14:0","63720C:15:0","63720C:16:0","63720C:17:0","63720C:22:0","63720C:23:0","63720C:32:0","63720C:33:0","63720C:34:0","63720C:35:0","63720C:38:0","63720C:39:0","701C94:0:0","701C94:1:0","701C94:2:0","701C94:3:0","701C94:4:0","701C94:5:0","701C94:6:0","701C94:7:0","701C94:8:0","701C94:9:0","701C94:10:0","701C94:11:0","701C94:12:0","701C94:13:0","701C94:14:0","701C94:15:0","701C94:16:0","701C94:17:0","701C94:18:0","701C94:19:0","701C94:20:0","701C94:21:0","701C94:22:0","701C94:23:0","701C94:24:0","701C94:25:0","701C94:26:0","701C94:27:0","70272C:0:0","70272C:1:0","70272C:2:0","70272C:3:0","70272C:4:0","70272C:5:0","70272C:6:0","70272C:7:0","70272C:8:0","70272C:9:0","70272C:10:0","70272C:11:0","70272C:12:0","703080:0:0","703080:1:0","703080:2:0","703080:3:0","703080:4:0","703080:5:0","703080:7:0","703080:8:0","703080:9:0","703080:10:0","703080:11:0","703080:12:0","70904C:2:0","70904C:24:0","70904C:25:0","70904C:26:0","70904C:27:0","70904C:30:0","70904C:31:0","70904C:32:0","70904C:33:0","70904C:34:0","70904C:50:0","70904C:51:0","70904C:52:0","70904C:53:0","70904C:54:0","70904C:55:0","70904C:56:0","70904C:57:0","70904C:58:0","70904C:59:0","70904C:60:0","70904C:61:0","70904C:62:0","70904C:73:0","70904C:74:0","70904C:79:0","70904C:80:0","70904C:81:0","70904C:82:0","70904C:83:0","70904C:84:0","70904C:85:0","70904C:88:0","70904C:100:0","70904C:101:0","70904C:102:0","70904C:103:0","70904C:104:0","70904C:105:0","70904C:106:0","70904C:107:0","70904C:108:0","709704:33:0","709704:34:0","709704:35:0","709704:36:0","709704:37:0","709704:38:0","709704:39:0","709704:40:0","709704:41:0","709704:42:0","709704:43:0","709704:44:0","709A34:0:0","709A34:1:0","709A34:5:0","709A34:10:0","709A34:15:0","709A34:20:0","709A34:25:0","709A34:30:0","709A34:35:0","709A34:40:0","709A34:45:0","709A34:50:0","709A34:55:0","709A34:60:0","709A34:65:0","709A34:70:0","709A34:75:0","709A34:80:0","709A34:85:0","709A34:90:0","709A34:95:0","709A34:100:0","709A34:105:0","709A34:110:0","709A34:115:0","709A34:120:0","709A34:121:0","709A34:125:0","709A34:130:0","709A34:131:0","709A34:132:0","709A34:135:0","709A34:140:0","709A34:145:0","71A37C:2:0","71BE98:2:0","765F68:0:0","765F70:0:0","76C918:0:0","76C92C:0:0"])
CONTEXT={
  "666430": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "673770": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "679424": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "682054": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "687910": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "703080": "Packed BBS author/title row with fixed-looking spaces; textual field meanings retained, nickname transliteration candidates unapproved; byte/cell offsets and consumer width NOT insertion-ready.",
  "709704": "PET description and item-name labels, explicitMegaMan for33..44; not item effects. Source/legacy item names separate from existing description consumer.",
  "768800": "Legacy soul-unison tutorial: explicitMrProgGreen teaches Lan; sacrifice terrain-destruction chip, regular prohibition, once/same-soul/battle,3turns,+30/B-charge/rapidfire preserved. Presence in ROM does NOT prove EXE4.5 supports soul-unison gameplay.",
  "6368E8": "Mixed shared UI/calendar/profile/debug labels and Latin/symbol table. Kana selector arrays2/3 NOT translated as prose; input model/page graphics separate, integration pending. Calendar cultural names retained, sibling gender composite candidates; !labels abbreviated referents unapproved.",
  "63720C": "Name honorific suffix table: kun/chan/sama/dono candidates군/양/님/공 need relationship and variable consumer review, not a global approved replacement.",
  "63746C": "Native PET quick-menu explanation, type3 box; not spoken Navi identity.",
  "65AAE0": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "65CC78": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "662C5C": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6684B0": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "66BE58": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "66DDD0": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6713B8": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6770B8": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "67CA84": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "67EA58": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6842F8": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "689DF8": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "68D96C": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "68FB1C": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "69561C": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "698A2C": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "69B134": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "69E61C": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6A0640": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6AA730": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6ACCA8": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6B6050": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6B8478": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6BC0C8": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6BE52C": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6C1BFC": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6C40AC": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6C7608": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6C982C": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6CCDC0": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6CF0A0": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6D2700": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6D44D4": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "6EAD18": "printShortString recipient suffix, translated에게candidate; recipient role/pointer consumer still needs integration review.",
  "701C94": "Packed BBS author/title row with fixed-looking spaces; textual field meanings retained, nickname transliteration candidates unapproved; byte/cell offsets and consumer width NOT insertion-ready.",
  "70272C": "Packed BBS author/title row with fixed-looking spaces; textual field meanings retained, nickname transliteration candidates unapproved; byte/cell offsets and consumer width NOT insertion-ready.",
  "70904C": "Mixed profile/date/gender/job input labels, packed field tables, setup Navi confirmation and item43/41 effect-end notices. Item/name/date/digit insertions and native options preserved; packed boundaries require consumer review.",
  "7097D8": "Developer false/test message: literal x prefix retained; not actual player guidance.",
  "709A34": "PA ingredient list with padded lines/packed triples. Same chip candidates as existing library where verified. Source digits and all per-line padding retained; no recipe or execution changes.",
  "709D88": "Prototype MegaMan daily/schedule/continue/new-cycle selector; buffer1 loop count preserved, actual reachability unverified.",
  "71A37C": "Numeric fixed cell count template:0123456789 and[z] immutable; suffix translated개, native consumer width unverified.",
  "71BE98": "Packed chip-name example/demo string; HI preserved literally, segmentation/storage unknown; not actual chip name table.",
  "765F68": "Legacy label Duo/GrandPrixPower; textual name candidate only, not new boss or function support.",
  "765F70": "Legacy label Duo/GrandPrixPower; textual name candidate only, not new boss or function support.",
  "76C918": "Legacy label Duo/GrandPrixPower; textual name candidate only, not new boss or function support.",
  "76C92C": "Legacy label Duo/GrandPrixPower; textual name candidate only, not new boss or function support.",
  "7794EC": "Developer/debug mixed give/take/register/mail/homepage/state setup messages. Commands can grant items/currency/all chips and alterflags; never executed. Native item labels and literal messages translated, not recast as normal progression.",
  "78B588": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78B610": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78B688": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78B784": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78B878": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78B8F0": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78B96C": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78B9E8": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78BA60": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78BAE4": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78BB64": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78BBDC": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78BC58": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78BCD8": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78BD54": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78BDC4": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78BE3C": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "78BEB8": "Explicit per-Navi dark-area warnings; portrait and nickname boundaries preserved. Comparing area toUnder not equating; voices are review candidates.",
  "79C240": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "79C8D8": "Placeholder or internal error-report literal; provisional meaning retained, sheet report not invented bug fix/user service. Portrait/reachability unknown, not normal Navi dialogue.",
  "7ADB90": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7ADCA4": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7AE01C": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7AEEC0": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7AEF4C": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7AF098": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7AF2F8": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7AF624": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B02AC": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B03C4": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B0488": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B0574": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B0978": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B19A8": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B1A54": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B1AC4": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B1BC0": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B1C78": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B1F44": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B3120": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B3C30": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B3E60": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B3FF0": "HeelNaviBlack encounter/accept/reject/victory/loss, choicewidth9/default0; battle setup globals/flags preserved.",
  "7B4184": "ShadowMan encounter, navi16 mirror-specific branch, player choices, revenge/three-river death threat; exact branch/width13/11/battle flags native unchanged."
}
SEMANTIC_REVIEW=[
  "Remaining515catalog units reconciled:500manual drafts(batch046)+13manual drafts(final047);2kana selector arrays remain unresolved structural input targets, not silently excluded from denominator. Not513unique sentences; no ROM writes.",
  "All selected source literals and native selected-script skeletons read, exact repeated WAIT_FALSE/CLEAR blocks abbreviated only in read-only logical view. Allsource IDs/TPL/payload/digits/brackets/line topology/padding/native commands preserved.",
  "Manual source-conditioned free prose. No automated prose generation, selection or shortening. New voices/terms/cultural names/honorifics/packed field segmentation need independent/human review; allneeds_review releasefalse.",
  "513translated strings include developer/prototype/soul-unison/legacy labels. Presence inROM is not proof of normal reachability or support; debug granting/save-affecting commands never executed.",
  "Packed BBS/profile/PA/Latin table byte/cell boundaries unresolved. Draft-first assets are not insertion-ready; 132px heuristic cannot approve/shorten or establish actual capacity.",
  "Name-entry source6368E8scripts2/3 are originalkana selector arrays; adopted40jamo page/composer is separate. Changing literal text cannot integrate selectors/rendering/commit/redisplay/persistence. Keep2original units untranslated until structural integration.",
  "Explicit portraits, hide transitions and player choices preserved; no portrait inferred solely from text.source768800MrProgGreen/Lan;7C416CMrProgGreen thenKnightMan.7C9C44/7CAF40speakerunknown.",
  "Source digits:+30/3turn/1chip/STA002103203303/HP memory33/itemgrant etc immutable. Developerallchip/currency/profile flags and minigameflag5059 unchanged. No emulator/save/ROM/image/keyboard modifications.",
  "Current draft-first sequence continues into whole-corpus consumer/font/layout readiness then cumulativeROM/screen/save regression; human wording review/graphics/keyboard integration/persistence/release remainopen."
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
            speaker='ui-label';speaker_evidence='source UI/data/debug label; not normal spoken dialogue; consumer context in asset'
        elif x.key in CHOICES:
            speaker='player-choice';speaker_evidence='native option literal'
        else:
            speaker=portrait or 'speaker-unestablished'
            if False:raise AssertionError('no inherited portrait exception')
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait=portrait,portrait_visibility=visibility,speaker_evidence=speaker_evidence,context=CONTEXT[archive],
            variable_context='Native dynamic inserts/branch/choice/portrait/HP commands immutable; inline grammar/geometry/reachability/runtime unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='remaining-contextual-ui-debug-npc',
        context=CONTEXT[archive],voice='Manual source-conditioned drafts;explicit portrait where shown;unapproved terms and voices.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Source IDs/text/TPL/payload,commands,variables,newline/padding and unselected source immutable; no ROM/save writes.',
        batch_id='batch500-046',semantic_review=SEMANTIC_REVIEW,units=units)

def main():
    if sum(v[1] for v in SOURCES.values())!=500:raise ValueError('500 batch size')
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve batch asset '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
