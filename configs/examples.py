EXAMPLES = [
    {
        "question": "부산역 근처 돼지국밥 맛집 알려주세요.",
        "sql": "SELECT * FROM RESTAURANTS WHERE DISTRICT = '동구' AND MENU_NAME LIKE '%돼지국밥%' ORDER BY RATING DESC",
        "source": "restaurants",
    },
    {
        "question": "광안리 근처에서 아이들이랑 가기 좋은 식당 추천해주세요.",
        "sql": "SELECT * FROM RESTAURANTS WHERE DISTRICT = '수영구' AND MENU_FOR_CHILDREN_YN = True ORDER BY RATING DESC",
        "source": "restaurants",
    },
    {
        "question": "주차가능한 식당 알려주세요.",
        "sql": "SELECT * FROM RESTAURANTS WHERE PARKING_LON_YN = True ORDER BY RATING DESC",
        "source": "restaurants",
    },
    {
        "question": "아침먹을 수 있는 식당 알려주세요.",
        "sql": "SELECT * FROM RESTAURANTS WHERE BREAKFAST_YN = True ORDER BY RATING DESC",
        "source": "restaurants",
    },
    {
        "question": "예약가능한 밀면 맛집 알려주세요.",
        "sql": "SELECT * FROM RESTAURANTS WHERE MENU_NAME LIKE '%밀면%' and RESERVABLE = True ORDER BY RATING DESC",
        "source": "restaurants",
    },
    {
        "question": "서구에서 부모님 모시고 가기 좋은 자연관광지 추천해주세요",
        "sql": "SELECT * FROM TOURIST_SPOTS WHERE RECOMMENDED_GROUP LIKE '%부모%' and CATEGORY LIKE '%자연%",
        "source": "tourist_spots",
    },
    {
        "question": "사진찍기 좋은 관광지 알려주세요.",
        "sql": "SELECT * FROM TOURIST_SPOTS",
        "source": "tourist_spots",
    },
    {
        "question": "아이들이랑 가기 좋은 공원 추천해주세요.",
        "sql": "SELECT * FROM TOURIST_SPOTS WHERE CATEGORY LIKE '%공원%' and RECOMMENDED_GROUP LIKE '%아이%'",
        "source": "tourist_spots",
    },
    {
        "question": "봄에 가기 좋은 관광지 추천해주세요",
        "sql": "SELECT * FROM TOURIST_SPOTS WHERE SEASON_NM LIKE '%봄%'",
        "source": "tourist_spots",
    },
    {
        "question": "부산역 근처 관광지 추천해주세요",
        "sql": "SELECT * FROM TOURIST_SPOTS WHERE DISTRICT = '동구'",
        "source": "tourist_spots",
    },
    {
        "question": "광안리 근처 관광지 추천해주세요",
        "sql": "SELECT * FROM TOURIST_SPOTS WHERE DISTRICT = '사하구'",
        "source": "tourist_spots",
    },
    {
        "question": "해운대 근처 관광지 추천해주세요",
        "sql": "SELECT * FROM TOURIST_SPOTS WHERE DISTRICT = '해운대구'",
        "source": "tourist_spots",
    },
]
