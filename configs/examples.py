EXAMPLES = [
    {
        "question": "서울시 종로구 무악동에 있는 반려동물 카페를 알려주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%서울특별시%종로구%무악동%' AND CATEGORY_NM = '카페'",
        "source": "pet_places",
    },
    {
        "question": "부산시 동구에 있는 동물병원을 알려주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%부산광역시%동구%' AND CATEGORY_NM = '동물병원'",
        "source": "pet_places",
    },
    {
        "question": "강남에서 주차 가능한 카페를 알고 싶어요.",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%강남구%' AND CATEGORY_NM = '카페' AND PARKING_LOT_YN = 'Y'",
        "source": "pet_places",
    },
    {
        "question": "서울에 반려동물 입장이 가능한 미술관이 있나요?",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%서울특별시%' AND CATEGORY_NM = '미술관'",
        "source": "pet_places",
    },
    {
        "question": "부산시 해운대구에서 반려동물 동반 추가요금이 없는 호텔이 있나요?",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%부산광역시%해운대구%' AND CATEGORY_NM = '호텔' AND ADDITIONAL_CHARGE_ON_PET = '없음'",
        "source": "pet_places",
    },
    {
        "question": "강원도에 위치한 반려동물 동반 여행지를 추천해주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%강원도%' AND CATEGORY_NM = '여행지'",
        "source": "pet_places",
    },
    {
        "question": "제주도에서 반려동물 크기 제한이 없는 카페를 알고 싶어요.",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%제주특별자치도%' AND CATEGORY_NM = '카페' AND POSIBLE_PET_SIZE = '모두 가능'",
        "source": "pet_places",
    },
    {
        "question": "부산에 있는 추석 당일에 영업하는 약국 알려주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%부산광역시%' AND CATEGORY_NM = '동물약국' AND HOLIDAY_INFORMATION NOT LIKE '%추석 당일%'",
        "source": "pet_places",
    },
    {
        "question": "서울특별시 도봉구에서 반려동물 동반이 가능한 박물관을 찾고 싶어요.",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%서울특별시%도봉구%' AND CATEGORY_NM = '박물관'",
        "source": "pet_places",
    },
    {
        "question": "서울 강남구에서 운영시간이 24시간인 동물병원을 알려주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%서울특별시%강남구%' AND OPERATION_TIME LIKE '%00:00~24:00%'",
        "source": "pet_places",
    },
    {
        "question": "서울에서 주말에 운영하는 반려동물 카페를 추천해주세요.",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%서울특별시%' AND CATEGORY_NM = '카페' AND (OPERATION_TIME LIKE '%토%' AND OPERATION_TIME LIKE '%일요일%')",
        "source": "pet_places",
    },
    {
        "question": "부산에서 토요일에 운영하는 반려동물 미용 시설이 있나요?",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%부산광역시%' AND CATEGORY_NM = '미용' AND OPERATION_TIME LIKE '%토%'",
        "source": "pet_places",
    },
    {
        "question": "경기도에서 일요일에도 영업하는 반려동물 병원을 찾고 싶어요.",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%경기도%' AND CATEGORY_NM = '동물병원' AND OPERATION_TIME LIKE '%일요일%'",
        "source": "pet_places",
    },
    {
        "question": "서울 종로구에서 월요일에 운영하는 반려동물 약국이 있나요?",
        "sql": "SELECT * FROM PET_PLACES WHERE LAND_LOT_ADDRESS LIKE '%서울특별시%종로구%' AND CATEGORY_NM = '동물약국' AND OPERATION_TIME LIKE '%월%'",
        "source": "pet_places",
    },
    {
        "question": "서울시 종로구에 있는 키즈존이 있는 시설을 알려주세요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '서울특별시' AND SIGNGU_NM = '종로구' AND KIDS_ZONE_AT = 'Y'",
        "source": "children_places",
    },
    {
        "question": "부산시 해운대구에서 유모차 대여가 가능한 박물관을 찾고 싶어요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '부산광역시' AND SIGNGU_NM = '해운대구' AND CTGRY_THREE_NM = '박물관' AND STROLLER_LEND_AT = 'Y'",
        "source": "children_places",
    },
    {
        "question": "경기도에 위치한 무료 주차가 가능한 놀이공원을 알려주세요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '경기도' AND CTGRY_ONE_NM = '놀이공원' AND FRE_PARKNG_AT = 'Y'",
        "source": "children_places",
    },
    {
        "question": "서울특별시 강남구에서 연령 제한이 없는 관광지 추천해주세요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '서울특별시' AND SIGNGU_NM = '강남구' AND CTGRY_TWO_NM LIKE '%관광지%' AND ENTRN_POSBL_BN_VALUE = '연령제한없음'",
        "source": "children_places",
    },
    {
        "question": "부산광역시에서 장애인 화장실이 있는 전시관을 알려주세요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '부산광역시' AND CTGRY_TWO_NM = '전시/기념관' AND DSPSN_TOILET_AT = 'Y'",
        "source": "children_places",
    },
    {
        "question": "서울시 은평구에 있는 운영시간이 24시간인 키즈 시설을 추천해주세요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '서울특별시' AND SIGNGU_NM = '은평구' AND OPER_TIME LIKE '%00:00~24:00%' AND KIDS_ZONE_AT = 'Y'",
        "source": "children_places",
    },
    {
        "question": "경기도에서 휴일에 운영하는 키즈존이 있는 시설을 알려주세요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '경기도' AND RSTDE_GUID_CN = '연중무휴' AND KIDS_ZONE_AT = 'Y'",
        "source": "children_places",
    },
    {
        "question": "서울 강동구에서 수유실이 있는 미술관을 추천해주세요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '서울특별시' AND SIGNGU_NM = '강동구' AND CTGRY_THREE_NM LIKE '%미술관%' AND NRSGRM_AT = 'Y'",
        "source": "children_places",
    },
    {
        "question": "제주도 서귀포시에서 장애인 화장실과 유모차 대여가 모두 가능한 놀이공원을 찾고 싶어요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '제주특별자치도' AND SIGNGU_NM = '서귀포시' AND CTGRY_THREE_NM LIKE '%놀이공원%' AND DSPSN_TOILET_AT = 'Y' AND STROLLER_LEND_AT = 'Y'",
        "source": "children_places",
    },
    {
        "question": "서울시 도봉구에 있는 무료 주차 가능한 전시 공간을 추천해주세요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '서울특별시' AND SIGNGU_NM = '도봉구' AND CTGRY_ONE_NM LIKE '%전시%' AND FRE_PARKNG_AT = 'Y'",
        "source": "children_places",
    },
    {
        "question": "부산 남구에서 연령 제한이 없는 키즈존이 있는 놀이공원을 추천해주세요.",
        "sql": "SELECT * FROM children_places WHERE CTPRVN_NM = '부산광역시' AND SIGNGU_NM = '남구' AND CTGRY_THREE_NM LIKE '%놀이공원%' AND ENTRN_POSBL_BN_VALUE = '연령제한없음' AND KIDS_ZONE_AT = 'Y'",
        "source": "children_places",
    },
]
