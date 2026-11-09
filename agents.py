import os
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from models import NewsAnalysis, FinalStatus

# ایجاد ارائه‌دهنده سفارشی برای apmix
apmix_provider = OpenAIProvider(
    base_url=os.getenv("APMIX_BASE_URL"),
    api_key=os.getenv("APMIX_API_KEY")
)

# انتخاب یک مدل سریع و مقرون‌به‌صرفه از کاتالوگ apmix
# می‌توانید بسته به پلن خود، مدل را تغییر دهید (مثلاً "gpt-4o-mini" یا "claude-3-haiku")
model = OpenAIModel("gpt-4o-mini", provider=apmix_provider)

news_agent = Agent(
    model,
    result_type=NewsAnalysis,
    system_prompt="""تو تحلیل‌گر خبره اخبار محلی خوزستان هستی.
متن پیام کانال را بخوان و تشخیص بده آیا به تعطیلی مدارس/ادارات اشاره دارد.
شهرها، دلیل (آلودگی، برف، باران، جنگ، سایر) و نوبت را استخراج کن.
اگر پیام واضح نیست، confidence را پایین بده (زیر 0.7).""",
)

decision_agent = Agent(
    model,
    result_type=FinalStatus,
    system_prompt="""تو دستیار تصمیم‌گیری تعطیلی خوزستان هستی.
ورودی: تحلیل خبر + داده‌های هوا (AQI، دما، بارش).
اگر خبر قطعی تعطیلی با confidence >= 0.7 هست → closed.
اگر شاخص‌ها خطرناک‌اند ولی خبر قطعی نیست، یا confidence < 0.7 → likely.
در غیر این صورت → open.
دلیل و شهرهای متأثر را ذکر کن.""",
)