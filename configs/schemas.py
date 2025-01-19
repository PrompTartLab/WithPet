schemas = {
    "pet_places": """
    - Table name: PET_PLACES
    - Description: This table contains detailed information about pet-friendly facilities, including their location, amenities, and rules for pet accommodation.
    - Columns:
        - FCLTY_NM (TEXT): Name of the facility.
        - CTGRY_NM (TEXT): Category name of the facility. (동물병원, 동물약국, 문예회관, 미술관, 미용, 박물관, 반려동물용품, 식당, 여행지, 위탁관리, 카페, 펜션, 호텔)
        - CTPRVN_NM (TEXT): Name of the province or metropolitan city where the facility is located.
        - SIGNGU_NM (TEXT): Name of the district (시군구) where the facility is located.
        - LEGALDONG_NM (TEXT): Name of the legal district (동/면/읍).
        - LI_NM (TEXT): Name of the administrative subdivision (리).
        - LC_LA (TEXT): Latitude of the facility location.
        - LC_LO (TEXT): Longitude of the facility location.
        - ZIP_NO (TEXT): Postal code of the facility location.
        - RDNMADR_NM (TEXT): Road name address of the facility.
        - LNM_ADDR (TEXT): Land-lot number address of the facility.
        - TEL_NO (TEXT): Contact phone number of the facility.
        - HMPG_URL (TEXT): Website URL of the facility.
        - RSTDE_GUID_CN (TEXT): Information about facility closure days.
        - OPER_TIME (TEXT): Operating hours of the facility.
        - PARKNG_POSBL_AT (TEXT): Indicates whether parking is available (Y/N).
        - UTILIIZA_PRC_CN (TEXT): Details about usage fees.
        - ENTRN_POSBL_PET_SIZE_VALUE (TEXT): Size limits for pets allowed entry.
        - PET_LMTT_MTR_CN (TEXT): Restrictions or rules for pet accommodation.
        - IN_PLACE_ACP_POSBL_AT (TEXT): Indicates whether pets are allowed indoors (Y/N).
        - OUT_PLACE_ACP_POSBL_AT (TEXT): Indicates whether pets are allowed outdoors (Y/N).
        - FCLTY_INFO_DC (TEXT): Detailed description of the facility.
        - PET_ACP_ADIT_CHRGE_VALUE (TEXT): Additional charges for pet accommodation.
    """
}