import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="معلمو الحصة لغة عربية ملوي", layout="wide")

# --- دالة التنظيف وتوحيد الحروف ---
def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    
    # 1. توحيد الألف (أ، إ، آ -> ا)
    for char in ['أ', 'إ', 'آ']:
        text = text.replace(char, 'ا')
    
    # 2. توحيد الهاء والتاء المربوطة (ة -> ه)
    text = text.replace('ة', 'ه')
    
    # 3. توحيد الياء (ى -> ي)
    text = text.replace('ى', 'ي')
    
    return text

# --- واجهة الموقع ---
# العنوان مع الأيقونات الجديدة
st.title("معلمو الحصة لغة عربية ملوي 👨‍🏫🔍")
st.markdown("---")

try:
    # قراءة الملف
    df = pd.read_excel("data.xlsx")
    
    # تجهيز أعمدة البحث الخفية
    df['search_name'] = df['اسم المعلم'].apply(normalize_text)
    df['search_school'] = df['اسم المدرسة'].apply(normalize_text)

    # خانة البحث
    query = st.text_input("اكتب الاسم أو اسم المدرسة هنا :", placeholder="مثال: محمد احمد / مدرسة البرشا")

    # خيار العرض للموبايل
    is_mobile = st.checkbox("📱 عرض مخصص للموبايل (بطاقات)")

    if query:
        search_term = normalize_text(query)
        
        # البحث في الاسمين
        mask = df['search_name'].str.contains(search_term, case=False) | \
               df['search_school'].str.contains(search_term, case=False)
        
        result = df[mask]
        
        if not result.empty:
            st.success(f"تم العثور على {len(result)} نتيجة:")
            
            if is_mobile:
                # عرض الموبايل
                for index, row in result.iterrows():
                    with st.container():
                        st.subheader(f"👤 {row['اسم المعلم']}")
                        st.write(f"🏫 **المدرسة:** {row['اسم المدرسة']}")
                        st.write(f"📊 **الحصص:** {row['الحصص الفعلية الأسبوعية']}")
                        st.write(f"📍 **القطاع:** {row['القطاع']}")
                        
                        status = row.get('الحالة', 'غير محدد')
                        if 'مستمر' in str(status):
                            st.markdown(f"✅ **الحالة:** :green[{status}]")
                        else:
                            st.markdown(f"⚠️ **الحالة:** :red[{status}]")
                        st.markdown("---")
            else:
                # عرض الكمبيوتر
                st.dataframe(
                    result[['اسم المعلم', 'اسم المدرسة', 'الحصص الفعلية الأسبوعية', 'القطاع', 'الحالة']],
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.warning("لم يتم العثور على نتائج. تأكد من صحة الاسم.")

except Exception as e:
    st.error("حدث خطأ! تأكد من وجود ملف data.xlsx")
