**Project Title : Weather & Environment Dashboard ** 

**สมาชิกกลุ่ม:**

* แมน Project Manager / CI-CD (รหัสนักศึกษา 673380399-7)
* พลอย Automated Tester & QA (รหัสนักศึกษา 643020630-5
* ใบยอ Core Developer (รหัสนักศึกษา 643020651-7) 

#  Problem Statement 
## 🌦️ Problem Statement (Revised Version)
 People often struggle to access comprehensive and up-to-date weather and environmental data in one place. Information such as temperature, humidity, air quality (AQI), and other environmental indicators is usually scattered across multiple sources, making it difficult and time-consuming to gather and interpret. 
 This lack of centralized, easy-to-understand data makes it challenging for individuals to make informed daily decisions — especially for groups sensitive to environmental conditions, such as: 

* Outdoor workers and commuters 
* Individuals with asthma or other respiratory issues
* Fitness enthusiasts who exercise outdoors 

#  Proposed Solution 
## 🌍 Project Description (Revised for Weather & Environment Dashboard) 
 The Weather & Environment Dashboard is a user-friendly platform designed to integrate and display real-time environmental information in one place. 
 It combines data on: 
* Current weather conditions 
* Air Quality Index (AQI) 
* Environmental indicators such as humidity, UV index, and pollution levels 
The system retrieves data from reliable public APIs and presents it in a clear, visually engaging interface. 
 Users can:
* Search for data by current location or specific city 
* View environmental trends and health recommendations based on AQI and weather conditions 
* Plan outdoor or daily activities safely and more efficiently 
This dashboard helps users stay informed about environmental factors that may affect their health, comfort, and daily decisions. 
 
## 🌐 4. Domain 
* Data Analysis & Management Result 
* Dashboard App API 

## API(s) to Use 
API Name : Open-Meteo API 
Documentation : https://open-meteo.com/ 
API Name : wttr.in   
Documentation : wttr.in  
Data Types : ข้อมูลพยากรณ์อากาศปัจจุบัน (Current Weather)  
ข้อมูลพยากรณ์อากาศล่วงหน้า (Forecast Data)  
ข้อมูลการค้นหาเมือง (City Names / Suggestions)  
ข้อมูล UI session ชั่วคราว เช่น เมืองล่าสุดที่ค้นหา  API  

## 👥 Roles & Responsibilities 
1. แมน Project Manager / CI-CD (รหัสนักศึกษา 673380399-7) 
 หน้าที่: วางแผนการดำเนินงาน และสรุปรวบรวมข้อมูล 
- วางแผนและกำหนดขั้นตอนการทำงานของโครงการในแต่ละระยะ  
- ประสานงานระหว่างสมาชิกทีม เพื่อให้การทำงานเป็นไปตามกำหนดเวลา 
- ศึกษาและรวบรวมข้อมูลที่เกี่ยวข้องกับสภาพอากาศ สิ่งแวดล้อม และ API ที่จะนำมาใช้ในระบบ 
- จัดทำสรุปผลการดำเนินงานและรายงานความคืบหน้าของโครงการในแต่ละช่วง

2. ใบยอ Core Developer (รหัสนักศึกษา 643020651-7) 
 หน้าที่ : ออกแบบโครงสร้างการทำงานของระบบ 
- ออกแบบสถาปัตยกรรมของระบบ รวมถึงโครงสร้างฐานข้อมูลและการเชื่อมต่อ API 
- จัดทำแผนผังการทำงาน และแบบจำลองการออกแบบ  
- ออกแบบส่วนติดต่อผู้ใช้  ให้มีความเข้าใจง่ายและเหมาะสมกับกลุ่มผู้ใช้งาน 
- สนับสนุนทีมพัฒนาในการแปลงแบบออกแบบไปสู่การพัฒนาโค้ดจริง 

3. พลอย Automated Tester & QA (รหัสนักศึกษา 643020630-5) 
 หน้าที่ : พัฒนาโค้ดและเชื่อมต่อ API 
- พัฒนาโปรแกรมตามแบบโครงสร้างและดีไซน์ที่ทีมออกแบบกำหนด 
- เชื่อมต่อ API ภายนอก เช่น ข้อมูลสภาพอากาศและคุณภาพอากาศแบบเรียลไทม์ 
- ทดสอบระบบ  เพื่อให้การทำงานของแดชบอร์ดมีความถูกต้องและเสถียร 
- ปรับปรุงประสิทธิภาพการทำงานของระบบและสนับสนุนการนำเสนอผลงานขั้นสุดท้าย 

## 🚀 Features (MVP) 
- ค้นหา ชื่อจังหวัด,เมือง,ประเทศ ในภาษาไทยหรือภาษาก็ได้ที่ต้องการทราบถึงสภาพอากาศ 
- ทราบสภาพอากาศ ณ วันที่ค้นหาและล่วงหน้า 2 วัน รวมถึงอุณหภูมิสูงสุดและต่ำสุด 
- บอกสภาพอากาศ,อุณหภูมิ,ความชื้น ของชื่อเมืองที่เราค้นหา
