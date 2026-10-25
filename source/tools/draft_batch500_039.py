"""500 contextual subchip, progression and Internet4 NPC drafts; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
  "6F9B4C": [
    "9d525a4109ec3ae8582662580ac090e5adc798800a6ca303860cf43be13c6452",
    16,
    "translations/batch500_039_subchips_hints_6F9B4C_draft_ko.json"
  ],
  "6F9CA8": [
    "45bd4031bba85daa47320205b8a5090e5061ab522865077a951860151fe708a6",
    16,
    "translations/batch500_039_subchips_hints_6F9CA8_draft_ko.json"
  ],
  "6F9E00": [
    "a59c2888786971330efbd14862877ca9b3ac4e2f00d7b0a4863d5c4d3c12cc91",
    16,
    "translations/batch500_039_subchips_hints_6F9E00_draft_ko.json"
  ],
  "6F9F5C": [
    "7f7eafd6ff0a2a8841c847418029c1097ffb83e07c2538aa541c32c56c510424",
    16,
    "translations/batch500_039_subchips_hints_6F9F5C_draft_ko.json"
  ],
  "6FA0B8": [
    "04dd38e52ffb19bb31f40d59f9c6e3450aad402926a27cf87923f59f1d1f3946",
    16,
    "translations/batch500_039_subchips_hints_6FA0B8_draft_ko.json"
  ],
  "6FA228": [
    "d3b3593f52d132ea69425d239c0b9a6c72078f0b2997a718f3f769a599bfa543",
    16,
    "translations/batch500_039_subchips_hints_6FA228_draft_ko.json"
  ],
  "6FA388": [
    "9be81f7cb16cd8ba8e449c9d8ddd03b9abe6adf56d1a281f6ea7dccfae757f1c",
    16,
    "translations/batch500_039_subchips_hints_6FA388_draft_ko.json"
  ],
  "6FA4E4": [
    "4660a75c8684b93d97c4872e60fb5fddae3b78dfd10effd3f347d27588c3779e",
    16,
    "translations/batch500_039_subchips_hints_6FA4E4_draft_ko.json"
  ],
  "6FA654": [
    "f183b4d04300a94391940cd2cf8adba3c44bc035de8b64ad15d2596fd109896f",
    16,
    "translations/batch500_039_subchips_hints_6FA654_draft_ko.json"
  ],
  "6FA7B8": [
    "8e90a9a57b323080982c46f9bf29cfd135709452e72c420b3572a7f0bde589be",
    16,
    "translations/batch500_039_subchips_hints_6FA7B8_draft_ko.json"
  ],
  "6FA910": [
    "27e24a81630bbae6c735915ed0c5600d6983e17be5a97ffaaa6eabc543c4410e",
    16,
    "translations/batch500_039_subchips_hints_6FA910_draft_ko.json"
  ],
  "6FAA80": [
    "5918d222c071e4af9e528c453de1664dcbc7fc90d29c0d399e96f979cf01560b",
    16,
    "translations/batch500_039_subchips_hints_6FAA80_draft_ko.json"
  ],
  "6FABEC": [
    "6def74dd7f15d1869dfc4f3d3af354195bf11601b0f4309b8f2879bf12b9d43c",
    16,
    "translations/batch500_039_subchips_hints_6FABEC_draft_ko.json"
  ],
  "6FAD44": [
    "6e7de21a5a89496ac39de6dd28fee28fdb3a1e41e9b1b0599ed2706595aba3de",
    16,
    "translations/batch500_039_subchips_hints_6FAD44_draft_ko.json"
  ],
  "6FAEA0": [
    "363cb960bdf2e70539fe06cc831a8dce2496de41bb76e31e9b44b9e97947ba10",
    16,
    "translations/batch500_039_subchips_hints_6FAEA0_draft_ko.json"
  ],
  "6FB000": [
    "b1117ddb7ce7aa4adb653b64cc5dead90742146fdc3ccca009dc7a24d765c55d",
    16,
    "translations/batch500_039_subchips_hints_6FB000_draft_ko.json"
  ],
  "6FB164": [
    "7c5407df5f11c3776e3ddb9b6e9419525d770164083feb251f4f03d88db58ad2",
    16,
    "translations/batch500_039_subchips_hints_6FB164_draft_ko.json"
  ],
  "6FB2C4": [
    "f461e41c704a214d77a6836443f90a9ba434630fcd5a228c115ff73b48d4f64c",
    16,
    "translations/batch500_039_subchips_hints_6FB2C4_draft_ko.json"
  ],
  "6FB41C": [
    "981729918070678025f9ddabf6207576b0b9021907d0a7d8ffc9a29a17f751ce",
    16,
    "translations/batch500_039_subchips_hints_6FB41C_draft_ko.json"
  ],
  "6FB574": [
    "8bb2467e6f4be35b88ee80bdd319a881f64c501f7113be015ff64bfbc776fe91",
    16,
    "translations/batch500_039_subchips_hints_6FB574_draft_ko.json"
  ],
  "6FB6D4": [
    "c4d9d40b8ac40b10bbc83a1c7f12325f6ad3d4c0c29fbe3d9e0ffeb08671f44d",
    16,
    "translations/batch500_039_subchips_hints_6FB6D4_draft_ko.json"
  ],
  "78AAF0": [
    "8e0c8bcbc6a8acc6c2faa66228dcd344a1155820ebc96e202ab119016c82f19c",
    27,
    "translations/batch500_039_subchips_hints_78AAF0_draft_ko.json"
  ],
  "78AE58": [
    "b996e6942da8c98aa0740c7f3a127ac14257795a3789fd80dadbe77625124e01",
    27,
    "translations/batch500_039_subchips_hints_78AE58_draft_ko.json"
  ],
  "78B1C0": [
    "2408630ac78bd92b4bd7803d130bef7058c8ef16b49492fc553c4ad5d7eda16e",
    27,
    "translations/batch500_039_subchips_hints_78B1C0_draft_ko.json"
  ],
  "7A6990": [
    "ca13c7c5c41fa567ff2ad00b6b438a744f4edd219ff38209806c9a8a00ddb9ae",
    6,
    "translations/batch500_039_subchips_hints_7A6990_draft_ko.json"
  ],
  "7A7000": [
    "a0e6855cbd9dce2db6e4ba238f189e018548aca47102d4d90346a6bef71c0f4a",
    77,
    "translations/batch500_039_subchips_hints_7A7000_draft_ko.json"
  ]
}
DRAFT={
  "6F9B4C": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n쓰지 말자",
    "7:1": "」\n사용할까?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "록맨의 HP가\n50 회복됐다!",
    "9:0": "록맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이야?",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없어!",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았지?"
  },
  "6F9CA8": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n쓰지 말자!",
    "7:1": "」\n사용할까?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "롤의 HP가\n50 회복됐다!",
    "9:0": "롤의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이야?",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없어!",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았지?"
  },
  "6F9E00": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 쓰지 않고,\n아껴 둔다거스!",
    "7:1": "」\n사용할 거스?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "거츠맨의 HP가\n50 회복됐다!",
    "9:0": "거츠맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이다거스!",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없다거스!",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았다거스!"
  },
  "6F9F5C": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n사용할 필요가 없다",
    "7:1": "」\n사용하겠나?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "윈드맨의 HP가\n50 회복됐다!",
    "9:0": "윈드맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이다...",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없다...",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았다..."
  },
  "6FA0B8": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": ",\n지금은 아직 사용하지\n맙시다...",
    "7:1": "」\n사용하시겠습니까?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "서치맨의 HP가\n50 회복됐다!",
    "9:0": "서치맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중입니다...",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없습니다",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았습니다"
  },
  "6FA228": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n쓰지 말자",
    "7:1": "」\n사용할까?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "파이어맨의 HP가\n50 회복됐다!",
    "9:0": "파이어맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이잖아?",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없어!",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았잖아?"
  },
  "6FA388": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n사용할 필요가 없다",
    "7:1": "」\n사용하겠나?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "썬더맨의 HP가\n50 회복됐다!",
    "9:0": "썬더맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이다...",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없다...",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았다..."
  },
  "6FA4E4": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": ",\n지금은 아직 사용하지\n맙시다...",
    "7:1": "」\n사용하시겠습니까?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "브루스의 HP가\n50 회복됐다!",
    "9:0": "브루스의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중입니다...",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없습니다",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았습니다"
  },
  "6FA654": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직 쓰지\n않는 게 어떨까요?",
    "7:1": "」\n사용할까요?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "넘버맨의 HP가\n50 회복됐다!",
    "9:0": "넘버맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중인데요?",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없어요!",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았는데요?"
  },
  "6FA7B8": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n사용할 필요가 없다",
    "7:1": "」\n사용하겠나?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "메탈맨의 HP가\n50 회복됐다!",
    "9:0": "메탈맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이다...",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없다...",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았다..."
  },
  "6FA910": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 사용하지 않아도\n괜찮다...",
    "7:1": "」\n사용할까?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "정크맨의 HP가\n50 회복됐다!",
    "9:0": "정크맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이지?",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없다!",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았지?"
  },
  "6FAA80": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직 쓰지 않아도\n괜찮아퓨!",
    "7:1": "」\n사용할 거야퓨?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "아쿠아맨의 HP가\n50 회복됐다!",
    "9:0": "아쿠아맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n지금 사용 중이야퓨",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없어퓨!",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았어퓨!"
  },
  "6FABEC": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n사용할 필요가 없다",
    "7:1": "」\n사용하겠나?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "우드맨의 HP가\n50 회복됐다!",
    "9:0": "우드맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이다...",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없다...",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았다..."
  },
  "6FAD44": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n쓰지 말자",
    "7:1": "」\n사용할까?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "스타맨의 HP가\n50 회복됐다!",
    "9:0": "스타맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이야?",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없어!",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았지?"
  },
  "6FAEA0": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n사용할 필요가 없다",
    "7:1": "」\n사용하겠나?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "섀도맨의 HP가\n50 회복됐다!",
    "9:0": "섀도맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이다...",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없다...",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았느니라..."
  },
  "6FB000": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직 쓰지\n맙시다!",
    "7:1": "」\n사용하시겠소?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "나이트맨의 HP가\n50 회복됐다!",
    "9:0": "나이트맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이오?",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없소",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았소"
  },
  "6FB164": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n쓰지 말자",
    "7:1": "」\n사용할까?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "네이팜맨의 HP가\n50 회복됐다!",
    "9:0": "네이팜맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이잖아?",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없어!",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았잖아?"
  },
  "6FB2C4": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n쓰지 않을 거예요!",
    "7:1": "」\n사용할까요?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "아이스맨의 HP가\n50 회복됐다!",
    "9:0": "아이스맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이에요!",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없어요!",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았어요!"
  },
  "6FB41C": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n사용할 필요가 없다",
    "7:1": "」\n사용하겠나?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "일렉맨의 HP가\n50 회복됐다!",
    "9:0": "일렉맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이다",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없다",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았다"
  },
  "6FB574": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n쓰지 말자",
    "7:1": "」\n사용할까...\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "플랜트맨의 HP가\n50 회복됐다!",
    "9:0": "플랜트맨의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이야",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없어",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았지..."
  },
  "6FB6D4": {
    "0:0": "HP50 회복!",
    "1:0": "HP를 최대치까지\n회복!",
    "2:0": "잠시 동안\n약한 바이러스와\n마주치지 않게 된다",
    "3:0": "미스터리 데이터에\n설치된 함정을 해제한다",
    "4:0": "직전에 만났던\n적과 다시\n마주치기 쉬워진다",
    "5:0": "보안이 걸린\n미스터리 데이터를\n해석한다",
    "6:0": "지금은 아직\n사용할 필요가 없다",
    "7:1": "」\n사용하겠나?\n",
    "7:2": "예  ",
    "7:3": "아니요",
    "8:0": "포르테의 HP가\n50 회복됐다!",
    "9:0": "포르테의 HP가\n완전히 회복됐다!",
    "10:1": "」\n사용했다",
    "11:1": "」\n이미 사용 중이다...",
    "12:0": "잠긴\n미스터리 데이터가\n바로 앞에 없다...",
    "13:0": "이 에리어에 온 뒤로\n아직 바이러스와\n마주치지 않았다..."
  },
  "78AAF0": {
    "10:0": "일단 인터넷을\n탐색해 볼까...",
    "11:0": "견습 라이선스 시험,\n...보러 갈까",
    "12:0": "견습 라이선스 시험을\n보러 가 볼까...",
    "13:1": "」\n입수하겠다",
    "14:0": "견습 라이선스를\n받으러 갈까",
    "15:0": "견습 라이선스를\n어떻게든 얻었군...\n조금 쉴까?",
    "16:0": "인터넷3에서\n일어난 사건이\n신경 쓰이는군...",
    "17:0": "아까 쓰러뜨린 내비가\n그 사건의 범인이었던\n것 같군...",
    "17:1": "한번 플러그아웃\n할까...?",
    "18:0": "인터넷5에서\n일어난 사건이\n신경 쓰이는군...",
    "19:0": "인터넷7에서\n일어난 사건이\n신경 쓰이는군...",
    "20:0": "인터넷9에서\n일어난 사건이\n신경 쓰이는군...",
    "21:0": "인터넷10에서\n일어난 사건이\n신경 쓰이는군...",
    "22:0": "인터넷12에서\n일어난 사건이\n신경 쓰이는군...",
    "23:0": "블랙워크스에게서\n「마이너스키」를\n되찾겠다...",
    "24:0": "「마이너스키」는,\n다른 내비1체가 가진\n것 같군...",
    "25:0": "「마이너스키」를\n인터넷9에 있는\n내비에게 가져가자",
    "26:0": "오피셜 토너먼트의\n참가 접수장에\n가 볼까...",
    "27:0": "언더 인터넷으로 가자\n목표 내비의 표식은\n관이었지...",
    "28:0": ",\n오피셜 토너먼트에\n참가 신청하러 갈까",
    "29:0": "주말에는\n오피셜 토너먼트로군\n내 MAX파워를 보여 주지",
    "30:0": "오피셜 토너먼트,\n...짜릿한 울림이군",
    "31:0": "인터넷을 차분히,\n탐색해 볼까...",
    "32:0": ",\n오피셜 토너먼트\n예선을 보러 갈까",
    "33:0": ",\n아까 도착한\n메일을 읽어 보자",
    "34:0": "다음 주가 되면,\n오피셜 토너먼트에\n참가 신청하러 갈까...",
    "35:0": "목표 내비의 표식은\n관이었지..."
  },
  "78AE58": {
    "10:0": "차분히 인터넷을\n탐색해 볼까...",
    "11:0": "견습 라이선스 시험,\n봐 보지 않을래?",
    "12:0": "견습 라이선스 시험을\n보러 가 볼까?",
    "13:1": "」\n찾으러 갈까...",
    "14:0": "견습 라이선스를\n받으러 갈까...",
    "15:0": "견습 라이선스 시험,\n수고했어...\n조금 쉴래?",
    "16:0": "인터넷3에서\n일어난 사건이\n신경 쓰이네...",
    "17:0": "아까 쓰러뜨린 내비가\n그 사건의 범인이었던\n것 같네...",
    "17:1": "조금 피곤하겠지,\n한번 플러그아웃\n할까...?",
    "18:0": "인터넷5에서\n일어난 사건이\n신경 쓰이네...",
    "19:0": "인터넷7에서\n일어난 사건이\n신경 쓰이네...",
    "20:0": "인터넷9에서\n일어난 사건이\n신경 쓰이네...",
    "21:0": "인터넷10에서\n일어난 사건이\n신경 쓰이네...",
    "22:0": "인터넷12에서\n일어난 사건이\n신경 쓰이네...",
    "23:0": "블랙워크스에게서\n「마이너스키」를\n되찾으러 갈까",
    "24:0": "「마이너스키」는,\n다른 내비1체가 가진\n모양이네...",
    "25:0": "「마이너스키」를\n인터넷9에 있는\n내비에게 가져갈까",
    "26:0": "오피셜 토너먼트의\n참가 접수장에\n가 볼까...",
    "27:0": "언더 인터넷으로 가자\n목표 내비의 표식은\n관이었지...",
    "28:0": ",\n오피셜 토너먼트에\n참가 신청하러 갈까",
    "29:0": "주말에는\n오피셜 토너먼트야\n최고의 꽃을 피우자",
    "30:0": "오피셜 토너먼트,\n최고의 꽃을 피우기에\n어울리는 무대야",
    "31:0": "인터넷을 더 깊이\n탐색해 보자...",
    "32:0": ",\n오피셜 토너먼트\n예선을 보러 갈까",
    "33:0": ",\n아까 도착한 메일을\n읽어 보는 건 어때?",
    "34:0": "다음 주가 되면,\n오피셜 토너먼트에\n참가 신청하러 가자",
    "35:0": "목표 내비의 표식은\n관이었지..."
  },
  "78B1C0": {
    "10:0": "인터넷을\n돌아다닐까...",
    "11:0": "견습 라이선스 시험,\n심심풀이로\n봐 볼까...",
    "12:0": "견습 라이선스\n시험을 보러 갈까",
    "13:1": "」\n찾는 건가... 흥",
    "14:0": "견습 라이선스란 것을\n받으러 가야겠군",
    "15:0": "견습 라이선스라...\n시시한 여흥이었군\n플러그아웃하겠다...",
    "16:0": "인터넷3에서\n일어난 사건...\n조금은 즐길 수 있겠군",
    "17:0": "아까 쓰러뜨린 내비가\n그 사건의 범인이었던\n모양이군...",
    "17:1": "지루한 시간을 보냈군\n...돌아가겠다",
    "18:0": "인터넷5에서\n일어난 사건...\n조금은 즐길 수 있겠군",
    "19:0": "인터넷7에서\n일어난 사건...\n조금은 즐길 수 있겠군",
    "20:0": "인터넷9에서\n일어난 사건...\n조금은 즐길 수 있겠군",
    "21:0": "인터넷10에서\n일어난 사건...\n조금은 즐길 수 있겠군",
    "22:0": "인터넷12에서\n일어난 사건...\n조금은 즐길 수 있겠군",
    "23:0": "마이너스키를 되찾으면\n되는 거군...",
    "24:0": "「마이너스키」는,\n다른 내비1체가 가진\n모양이군...",
    "25:0": "「마이너스키」를\n인터넷9에 있는\n내비에게 가져가겠다...",
    "26:0": "오피셜 토너먼트의\n참가 접수장에\n가겠다...",
    "27:0": "언더 인터넷으로 가겠다...\n목표 내비의 표식은\n관이었지...",
    "28:0": ",\n오피셜 토너먼트에\n참가 신청하러 가겠다...",
    "29:0": "주말에는\n오피셜 토너먼트다",
    "30:0": "오피셜\n토너먼트다...",
    "31:0": "인터넷 탐색을\n계속하겠다...",
    "32:0": ",\n오피셜 토너먼트\n예선을 보러 가겠다...",
    "33:0": "아까 그 메일은\n무슨 내용이었지...?",
    "34:0": "다음 주가 되면,\n오피셜 토너먼트에\n참가 신청하러 가겠다...",
    "35:0": "목표 내비의 표식은\n관이었지..."
  },
  "7A6990": {
    "0:0": "음, 오늘도\n이상 없음!",
    "0:1": "너무 평화로워서,\n가끔은 사건 한두 개쯤\n일어났으면...",
    "0:2": "아니, 그럴 리가 있겠어!",
    "0:3": "평화가 최고!!",
    "1:0": "하~암!",
    "1:1": "정말, 지루한 에리어에\n배치되고 말았네"
  },
  "7A7000": {
    "0:0": "환영합니다!!\n여기는\n인터넷4입니다!!",
    "0:1": "오늘도 힘차게\n힘·내·보·자!!",
    "1:0": "안녀어어어어어엉!!\n여기는\n인터넷4입니다!!",
    "1:1": "여기는 평온한 에리어예요!\n느긋하게 쉬다 가세요!!",
    "2:0": "좋은 저녁이에요!!",
    "2:1": "너무 늦게까지\n놀면 안 돼요!",
    "3:0": "쿨, 쿨...",
    "3:1": "여기는,\n인터넷4...\n음냐음냐...",
    "10:0": "우오오오!!\n저도 넷 배틀\n하고 싶어요오오!!",
    "10:1": "프로그램에게는,\n토너먼트\n참가 자격이 없을까요?",
    "11:0": "넷 배틀하는\n내비 여러분을\n보고 있으면,",
    "11:1": "왠지,\n저도 배틀을\n해 보고 싶어져요",
    "11:2": "하지만...\n저는 프로그램이니...",
    "15:0": "이 에리어는 대부분의 사람들이\n그냥 통과하기만 하는 에리어야",
    "15:1": "저기 비탈길을 올라서\n앞으로 나아가면,\n인터넷5로 갈 수 있어",
    "30:0": "여어! 뜨거운 하루하루를\n보내고 있나!?",
    "30:1": "열기가 부족하다면,\n나랑 배틀하지 않겠나?",
    "30:2": "아주 뜨거워질 수 있다구?",
    "30:3": "응  ",
    "30:4": "그만둘래",
    "30:5": "열기가 필요할 때는\n나한테 와라!!",
    "31:0": "큭! 다 타 버렸군...",
    "32:0": "아직 열기가\n부족한 모양이군!!",
    "32:1": "더 뜨거워지지 않으면,\n나를 이길 수 없어!!!",
    "33:0": "안녕!\n나랑 배틀하지 않을래?",
    "33:1": "멋진 별똥별을,\n보여 줄게!!",
    "33:2": "할래!  ",
    "33:3": "안 할래!",
    "33:4": "쳇, 재미없어!",
    "34:0": "다, 당했다...",
    "34:1": "머리 위에서 별이\n반짝이고 있어~",
    "35:0": "어때, 별똥별은\n볼 수 있었어?",
    "36:0": "불타오른다!!",
    "36:1": "배틀 오퍼레이션, 세트으!",
    "36:2": "인!!",
    "37:0": "별똥별이여, 나에게 승리를!",
    "37:1": "배틀 오퍼레이션, 세트!\n인!!",
    "38:0": "네 녀석, 뭐 하는 놈이냐!?",
    "38:1": "쳇, 나랑 똑같은\n얼굴을 하고서는...\n불쾌하군!!",
    "38:2": "파이어맨은 나1명이면\n충분하다!!",
    "38:3": "어이, 나랑 배틀해라!",
    "38:4": "응  ",
    "38:5": "그만둘래",
    "38:6": "역시, 가짜였군...",
    "39:0": "세상에는 자신과\n얼굴이 같은 사람이3명 있다고\n흔히 말하는데,",
    "39:1": "신기한 일도\n있구나!",
    "39:2": "어때, 나랑 배틀할래?",
    "39:3": "할래!  ",
    "39:4": "안 할래!",
    "39:5": "쳇, 재미없어!",
    "50:0": "최근 다크로이드라\n자칭하는 흉악한 내비가\n출몰하고 있어",
    "50:1": "각별히 조심하도록!",
    "51:0": "다크로이드는 어디로\n도망간 거지...?",
    "52:0": "다크로이드가 언더에\n잠복해 있다는\n정보가 있지만...",
    "52:1": "언더에서는\n손대기가 어렵군...",
    "53:0": "오피셜 토너먼트에서\n우승한 내비가\n다크로이드를 쓰러뜨렸다는군",
    "53:1": "하지만, 녀석들은\n신출귀몰...",
    "53:2": "삭제되더라도\n다시 살아날지도 몰라",
    "53:3": "방심할 수 없겠군...",
    "80:0": "잠깐, 잠깐!\n거기 당신!",
    "80:2": "」\n갖고 싶지 않아?",
    "80:3": "인터넷2와\n인터넷3 사이를\n막고 있는 문의 열쇠야!",
    "80:4": "지금은 단돈\n500제니!!",
    "80:5": "자, 살 거야!?",
    "80:6": "살래!  ",
    "80:7": "싫어!",
    "80:8": "그러신가...",
    "80:9": "또 마음이 바뀌면\n찾아와...",
    "82:0": "손님,\n돈이 조금\n부족하네...",
    "82:1": "나도 빠듯한\n가격으로 팔고 있어서\n이건 깎아 줄 수 없겠어",
    "82:2": "미안하지만,\n다시 와 줘",
    "83:0": "...새로운 사업을\n좀 더 생각해 봐야겠군\n......",
    "84:0": "오오, 씀씀이가 좋군,\n손님!",
    "84:1": "그럼 상품을\n전해 줄게, 받아!",
    "84:2": ":\n「",
    "84:3": "」\n획득했다!!",
    "84:4": "고마워!!\n당신, 좋은 물건을 샀어!"
  }
}
EXCLUDED=set()
CHOICES=set(["6F9B4C:7:2","6F9B4C:7:3","6F9CA8:7:2","6F9CA8:7:3","6F9E00:7:2","6F9E00:7:3","6F9F5C:7:2","6F9F5C:7:3","6FA0B8:7:2","6FA0B8:7:3","6FA228:7:2","6FA228:7:3","6FA388:7:2","6FA388:7:3","6FA4E4:7:2","6FA4E4:7:3","6FA654:7:2","6FA654:7:3","6FA7B8:7:2","6FA7B8:7:3","6FA910:7:2","6FA910:7:3","6FAA80:7:2","6FAA80:7:3","6FABEC:7:2","6FABEC:7:3","6FAD44:7:2","6FAD44:7:3","6FAEA0:7:2","6FAEA0:7:3","6FB000:7:2","6FB000:7:3","6FB164:7:2","6FB164:7:3","6FB2C4:7:2","6FB2C4:7:3","6FB41C:7:2","6FB41C:7:3","6FB574:7:2","6FB574:7:3","6FB6D4:7:2","6FB6D4:7:3","7A7000:30:3","7A7000:30:4","7A7000:33:2","7A7000:33:3","7A7000:38:4","7A7000:38:5","7A7000:39:3","7A7000:39:4","7A7000:80:6","7A7000:80:7"])
LABELS=set(["6F9B4C:0:0","6F9B4C:1:0","6F9B4C:2:0","6F9B4C:3:0","6F9B4C:4:0","6F9B4C:5:0","6F9CA8:0:0","6F9CA8:1:0","6F9CA8:2:0","6F9CA8:3:0","6F9CA8:4:0","6F9CA8:5:0","6F9E00:0:0","6F9E00:1:0","6F9E00:2:0","6F9E00:3:0","6F9E00:4:0","6F9E00:5:0","6F9F5C:0:0","6F9F5C:1:0","6F9F5C:2:0","6F9F5C:3:0","6F9F5C:4:0","6F9F5C:5:0","6FA0B8:0:0","6FA0B8:1:0","6FA0B8:2:0","6FA0B8:3:0","6FA0B8:4:0","6FA0B8:5:0","6FA228:0:0","6FA228:1:0","6FA228:2:0","6FA228:3:0","6FA228:4:0","6FA228:5:0","6FA388:0:0","6FA388:1:0","6FA388:2:0","6FA388:3:0","6FA388:4:0","6FA388:5:0","6FA4E4:0:0","6FA4E4:1:0","6FA4E4:2:0","6FA4E4:3:0","6FA4E4:4:0","6FA4E4:5:0","6FA654:0:0","6FA654:1:0","6FA654:2:0","6FA654:3:0","6FA654:4:0","6FA654:5:0","6FA7B8:0:0","6FA7B8:1:0","6FA7B8:2:0","6FA7B8:3:0","6FA7B8:4:0","6FA7B8:5:0","6FA910:0:0","6FA910:1:0","6FA910:2:0","6FA910:3:0","6FA910:4:0","6FA910:5:0","6FAA80:0:0","6FAA80:1:0","6FAA80:2:0","6FAA80:3:0","6FAA80:4:0","6FAA80:5:0","6FABEC:0:0","6FABEC:1:0","6FABEC:2:0","6FABEC:3:0","6FABEC:4:0","6FABEC:5:0","6FAD44:0:0","6FAD44:1:0","6FAD44:2:0","6FAD44:3:0","6FAD44:4:0","6FAD44:5:0","6FAEA0:0:0","6FAEA0:1:0","6FAEA0:2:0","6FAEA0:3:0","6FAEA0:4:0","6FAEA0:5:0","6FB000:0:0","6FB000:1:0","6FB000:2:0","6FB000:3:0","6FB000:4:0","6FB000:5:0","6FB164:0:0","6FB164:1:0","6FB164:2:0","6FB164:3:0","6FB164:4:0","6FB164:5:0","6FB2C4:0:0","6FB2C4:1:0","6FB2C4:2:0","6FB2C4:3:0","6FB2C4:4:0","6FB2C4:5:0","6FB41C:0:0","6FB41C:1:0","6FB41C:2:0","6FB41C:3:0","6FB41C:4:0","6FB41C:5:0","6FB574:0:0","6FB574:1:0","6FB574:2:0","6FB574:3:0","6FB574:4:0","6FB574:5:0","6FB6D4:0:0","6FB6D4:1:0","6FB6D4:2:0","6FB6D4:3:0","6FB6D4:4:0","6FB6D4:5:0"])
CONTEXT={
  "6F9B4C": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with MegaMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6F9CA8": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with Roll portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6F9E00": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with GutsMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6F9F5C": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with WindMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FA0B8": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with SearchMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. Script6 nickname insertion;comma boundary preserved. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FA228": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with FireMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FA388": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with ThunderMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FA4E4": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with ProtoMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. Script6 nickname insertion;comma boundary preserved. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FA654": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with NumberMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FA7B8": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with MetalMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FA910": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with JunkMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FAA80": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with AquaMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FABEC": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with WoodMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FAD44": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with StarMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FAEA0": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with ShadowMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FB000": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with KnightMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FB164": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with NapalmMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FB2C4": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with IceMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FB41C": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with ElecMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FB574": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with PlantMan portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "6FB6D4": "Native subchip descriptions0..5 mmbn45s distinct from quick dialogue6/7/11/12/13 with Bass portrait. Recovery50HP versus fullHP results8/9 and used-item10 have no local portrait assignment. item0 buffer1 split quotes,script7 width8/default0/two choices;sourcecommands do not implement effect here. Weak-virus avoidance not all-virus immunity,lastencounter probability not guaranteedfight,trap removal versus security analysis. No invented nickname insertion. Existing voices remain review candidates;JunkMan here has no source stutter,not added.",
  "78AAF0": "ElecMan progression0/10..35,flags82/9064..9070/9576..9582. Native priority tournament4/Shade4270/item11/BlackWorks/case/apprentice;Internet3/5/7/9/10/12 and key delivery9,coffin clue,weekday0/6,subarea0..3,chip104 and nickname. MAXpower and electric thrilling metaphor.",
  "78AE58": "PlantMan progression0/10..35,flags86/9072..9078/9584..9590. Same native branch context as78AAF0;gentle invitations and highestflower championship-stage metaphor,not battle reward or actual flower item. Dynamicchip104/nickname boundaries retained.",
  "78B1C0": "Bass progression0/10..35,flags90/9080..9086/9592..9598. Same native case/licence/key/tournament priority;contemptuous examination amusement and case entertainment,not concerned sympathy. Script33 no nickname insertion unlike Elec/Plant;source nickname28 vocative avoids받침dependency.",
  "7A6990": "OfficialNavi peace-and-boredom NPC,complete scripts0/1. Mock wish for one or two cases immediately retracted with peacebest;no actual incident or crime request.",
  "7A7000": "Internet4 NPC completeTPL:MrProg welcome/day-night/sleep/battlewish,Yellow passage slope Internet5,FireMan battles30/31/32/36/38 checkNavi5,StarMan33/34/35/37/39 checkNavi15. Hidden battlechoices widths9/11,globals24..28 and flags1806/7701 unchanged. OfficialNavi Darkloid rumours51/52/53 with cleared/licence flags;possible resurrection not certainty. Yellow item5 keymerchant500Zenny,checkItem5 ownership83,checkTakeZenny500 failure82,itemGive5 one,hidden currentNavi/item acquisition84. Native10choices with padding,no new tradingfunction."
}
SEMANTIC_REVIEW=[
  "Exactly500Japanese stable catalog literals in26complete archives:336subchip descriptions/use prompts/results,81remaining3Navi progression hints,6OfficialNPC and77Internet4NPC/battlers/merchant. Nativechoices52,subchipdescriptionlabels126,unresolved excludes0;no placeholder padding.",
  "Allselected source literals manually read in local contexts;full6F9B4C/78AAF0 plus exact per-script control differences for20subchip and2progressionarchives,full7A6990/7A7000. Source identity/rawTPL/payload and commands not recreated from translator output.",
  "needs_review development-draft NON-DISTRIBUTION releasefalse;originalROM/currentbaselineROM,save,emulator,graphics,keyboard unchanged. Source-controlled numbers/control/newline/padding/quote boundaries immutable.",
  "Subchip0..5 function descriptions do not speak in Navi voice:HP50/fullHP,temporaryweakvirus avoidance,trapremoval,lastencounterincreasedprobability,securityanalysis. Quickrecovery8/9 names explicit;no localportrait in8/9/10,not assigned specific current speakingNavi.",
  "Item0buffer1/name and chip104 dynamic prefixes preserved;closing-quote/newline clauses avoid fixedobjectparticles. Names after currentNavi in purchase usecolon,notfixed은/는;nicknamecomma no fixedvocative. Script7 trailingnewline and paddedchoices preserved.",
  "Character voices draft candidates,sourceJunkMan subchips do not stutter so no extrapolated stutter. ElecMAXpower/Plantbestflower/Basscontempt and no nickname inBass33 preserved independently;prior translation variants not automatically harmonized.",
  "Internet4 slope to5,item5 keybetween2/3,500Zenny deduction versus insufficientmoney and1itemgift,owneditemexit,Fire/Star sameNavi5/15 responses,threepeoplefolklore andoneFireperson preserved. Battle startglobals/flags unchanged;not directly execute battles/trades.",
  "OfficialDarkloid evidence remains rumours and possible resurrection;cleared/licencepriority kept. PeaceNPC mock casewish immediately denies it,no invented mission. Cultural/exclamation/voice/name terminology pending human review.",
  "Passing glyph/codec/control/skeleton and132px heuristic is not semantic approval or actualconsumer/runtime proof. Complete drafting then font/layout/insertion validation,cumulativeROM integration/screens/save/keyboard/images/release remain pending."
]
def authored(archive):return DRAFT[archive]
def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    plan=json.loads((ROOT/'translations/full_translation_first_plan.json').read_text(encoding='utf8'))
    require_hash(ROOT/plan['source_inventory']['path'],plan['source_inventory']['sha256'])
    catalog=json.loads((ROOT/plan['source_inventory']['path']).read_text(encoding='utf8'))
    ids={u['id'] for u in catalog['units'] if u['archive']==archive and u['status']=='unselected_japanese'}-EXCLUDED
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
            speaker='ui-label';speaker_evidence='native mmbn45s subchip description; not spoken dialogue or choice'
        elif x.key in CHOICES:
            speaker='player-choice';speaker_evidence='native option literal'
        else:speaker=portrait or 'speaker-unestablished'
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait=portrait,portrait_visibility=visibility,speaker_evidence=speaker_evidence,context=CONTEXT[archive],
            variable_context='Native item0buffer1/currentNavi/item5/chip104/nickname insertions and subchip choices,licence/case/weekday branches,battleglobals and merchant500Zenny protected. Capacity/routing/runtime unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='batch500-contextual-subchip-progress-internet4',
        context=CONTEXT[archive],voice='Manual source-conditioned drafts;explicit portrait where shown;unapproved terms and voices.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Source IDs/text/TPL/payload,commands,variables,newline/padding and unselected source immutable; no ROM/save writes.',
        batch_id='batch500-039',semantic_review=SEMANTIC_REVIEW,units=units)

def main():
    if sum(v[1] for v in SOURCES.values())!=500:raise ValueError('500 batch size')
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve batch asset '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()

