schemas = {
    "local_tourist_spots": """
        - Description: This table contains information about tourist spots for local visitors.
        - Columns:
            - Tourist_Spot_Name_Korean (TEXT): The name of the tourist spot in Korean.
            - District (TEXT): The district (구) where the tourist spot is located.
            - Major_Category (CATEGORICAL): The category of the tourist spot. Possible values: ['역사관광지', '건축/조형물', '휴양관광지', '쇼핑', '체험관광지', '자연관광지', '육상 레포츠', '음식점', '문화시설', '산업관광지', '숙박시설', '수상 레포츠', '레포츠소개'].
            - Number_of_Visit (INTEGER): The number of visitors to the tourist spot.
    """,
    "foreign_tourist_spots": """
        - Description: This table contains information about tourist spots for foreign visitors.
        - Columns:
            - Tourist_Spot_Name_English (TEXT): The name of the tourist spot in English.
            - Tourist_Spot_Name_Korean (TEXT): The name of the tourist spot in Korean.
            - District (TEXT): The district (구) where the tourist spot is located.
            - Major_Category (CATEGORICAL): The category of the tourist spot. Possible values: ['역사관광지', '휴양관광지', '체험관광지', '쇼핑', '자연관광지', '건축/조형물', '육상 레포츠', '산업관광지', '문화시설', '수상 레포츠', '음식점', '공연/행사', '숙박시설', '레포츠소개'].
            - Number_of_Visit (INTEGER): The number of visitors to the tourist spot.
    """,
    "restaurants": """
        - Description: This table contains information about popular restaurants in Busan.
        - Columns:
            - MENU_TYPE (TEXT): The type of menu offered at the restaurant (e.g., 한식, 중식, 분식).
            - RESTAURANT_NAME_KOREAN (TEXT): The Korean name of the restaurant.
            - ADDRESS_KOREAN (TEXT): The Korean address of the restaurant.
            - MENU_NAME (TEXT): The list of menu items offered by the restaurant.
            - DISTRICT_NAME (TEXT): The district (구) where the restaurant is located.
            - LATITUDE (REAL): The latitude of the restaurant.
            - LONGITUDE (REAL): The longitude of the restaurant.
            - RATING (REAL): The rating of the restaurant (out of 5).
            - RATING_COUNT (INTEGER): The number of reviews that contributed to the restaurant's rating.
            - PRICE_LEVEL (INTEGER): The price level of the restaurant (1 = low, 2 = medium, 3 = high).
            - TAKEOUT_YN (BOOLEAN): Whether the restaurant offers takeout (True/False).
            - RESERVABLE (BOOLEAN): Whether the restaurant accepts reservations (True/False).
            - BREAKFAST_YN (BOOLEAN): Whether breakfast is served (True/False).
            - LUNCH_YN (BOOLEAN): Whether lunch is served (True/False).
            - DINNER_YN (BOOLEAN): Whether dinner is served (True/False).
            - BEER_YN (BOOLEAN): Whether the restaurant serves beer (True/False).
            - OUTDOOR_SEAT_YN (BOOLEAN): Whether the restaurant has outdoor seating (True/False).
            - MENU_FOR_CHILDREN_YN (BOOLEAN): Whether the restaurant offers a children's menu (True/False).
            - RESTROOM_YN (BOOLEAN): Whether the restaurant has restrooms (True/False).
            - PARKING_LOT_YN (BOOLEAN): Whether the restaurant provides parking (True/False).
            - PAYMENT_OPTIONS (TEXT): Payment options available (e.g., credit cards).
            - REVIEW (TEXT): Customer reviews for the restaurant.
""",
}
