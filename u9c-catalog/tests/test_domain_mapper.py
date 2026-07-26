from u9c_catalog.domain_mapper import assign_domain
from u9c_catalog.models import TableMeta


def _t(name):
    return TableMeta(schema="dbo", name=name, object_type="TABLE")


def test_production_prefix():
    d = assign_domain(_t("MO_IssueDocLine"))
    assert d.domain == "생산실적"
    assert d.confidence >= 0.5
    assert "MO_" in d.evidence


def test_inventory_prefix():
    assert assign_domain(_t("InvTrans_TransLine")).domain == "입출고"
    assert assign_domain(_t("InvDoc_TransInBin")).domain == "입출고"


def test_sales_and_purchase_and_cost():
    assert assign_domain(_t("SM_SOOrder")).domain == "매출"
    assert assign_domain(_t("PM_Receivement")).domain == "구매"
    assert assign_domain(_t("GL_Entry")).domain == "비용등록"


def test_requisition_keyword_beats_generic_pm():
    d = assign_domain(_t("PM_PurchaseRequisition"))
    assert d.domain == "구매요청"


def test_platform_and_unknown():
    assert assign_domain(_t("UBF_MD_Attribute")).domain == "미분류"
    assert assign_domain(_t("ZZ_Something")).domain == "미분류"
