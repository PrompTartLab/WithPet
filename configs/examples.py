EXAMPLES = [
    {
        "question": "서울시 종로구 무악동에 있는 반려동물 카페를 알려주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '서울특별시' AND SIGNGU_NM = '종로구' AND LEGALDONG_NM = '무악동' AND CTGRY_NM = '카페'",
        "source": "pet_places",
    },
    {
        "question": "부산시 동구에 있는 동물병원을 알려주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '부산광역시' AND SIGNGU_NM = '동구' AND CTGRY_NM = '동물병원'",
        "source": "pet_places",
    },
    {
        "question": "서울시 강남구에서 주차 가능한 카페를 알고 싶어요.",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '서울특별시' AND SIGNGU_NM = '강남구' AND CTGRY_NM = '카페' AND PARKNG_POSBL_AT = 'Y'",
        "source": "pet_places",
    },
    {
        "question": "서울에 반려동물 입장이 가능한 미술관이 있나요?",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '서울특별시' AND CTGRY_NM = '미술관'",
        "source": "pet_places",
    },
    {
        "question": "부산시 해운대구에서 반려동물 동반 추가요금이 없는 호텔이 있나요?",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '부산광역시' AND SIGNGU_NM = '해운대구' AND CTGRY_NM = '호텔' AND PET_ACP_ADIT_CHRGE_VALUE = '없음'",
        "source": "pet_places",
    },
    {
        "question": "강원도에 위치한 반려동물 동반 여행지를 추천해주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '강원도' AND CTGRY_NM = '여행지'",
        "source": "pet_places",
    },
    {
        "question": "제주도에서 반려동물 크기 제한이 없는 카페를 알고 싶어요.",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '제주특별자치도' AND CTGRY_NM = '카페' AND ENTRN_POSBL_PET_SIZE_VALUE = '모두 가능'",
        "source": "pet_places",
    },
    {
        "question": "부산에 있는 추석 당일에 영업하는 약국 알려주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '부산광역시' AND CTGRY_NM = '동물약국' AND RSTDE_GUID_CN NOT LIKE '%추석 당일%'",
        "source": "pet_places",
    },
    {
        "question": "서울특별시 도봉구에서 반려동물 동반이 가능한 박물관을 찾고 싶어요.",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '서울특별시' AND SIGNGU_NM = '도봉구' AND CTGRY_NM = '박물관'",
        "source": "pet_places",
    },
    {
        "question": "제주도에서 반려동물 동반이 가능한 식당을 알고 싶어요.",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '제주특별자치도' AND CTGRY_NM = '식당'",
        "source": "pet_places",
    },
    {
        "question": "서울 강남구에서 운영시간이 24시간인 동물병원을 알려주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE CTPRVN_NM = '서울특별시' AND SIGNGU_NM = '강남구' AND OPER_TIME = '매일 00:00~24:00'",
        "source": "pet_places",
    },
]
