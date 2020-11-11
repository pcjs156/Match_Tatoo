from .models import Matching


# GET으로 받아온 매칭 검색 조건이 유효한지 검사
def searching_keyword_validation(region, tattoo_type, part, orderby) -> dict:
    ret = dict()

    region_choices = (pair[1] for pair in Matching.REGION)
    ret["region"] = (region in region_choices) and (region != "지역")

    tattoo_type_choices = (pair[1] for pair in Matching.TYPE)
    ret["tattoo_type"] = tattoo_type in tattoo_type_choices

    part_choices = (pair[1] for pair in Matching.PART)
    ret["part"] = part in part_choices

    orderby_choices = ("price", "pub-date")
    ret["order-by"] = orderby in orderby_choices

    return ret
