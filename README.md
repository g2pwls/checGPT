# AI 기반 도서 및 콘텐츠 추천 플랫폼

## 📚 프로젝트 소개

우리 서비스는 **AI 기반 도서 추천**과 **사용자 커뮤니티 기능**을 결합하여 독서 경험을 한층 더 확장하고 풍부하게 만들어주는 플랫폼입니다.  

기존의 단순한 "도서 검색·조회" 서비스를 넘어, 사용자가 원하는 **분위기나 감성**을 입력하면 AI가 이를 분석해 가장 어울리는 책을 3권 추천합니다.  
이를 통해 사용자는 자신이 몰랐던 새로운 책을 발견할 수 있으며, **정확도 높은 맞춤형 추천 경험**을 누릴 수 있습니다.  

또한, 좋아요 수가 일정 기준 이상 모인 책은 자동으로 **팬 커뮤니티**가 생성됩니다.  
이곳에서 사용자들은 책에 대한 감상과 생각을 자유롭게 공유하고, 댓글·스레드 기능을 통해 깊이 있는 토론을 이어갈 수 있습니다.  



### 🌟 주요 특징
- **AI 감성 분석 기반 추천**  
  - 단순 키워드가 아닌 "분위기·느낌"에 따라 책을 찾아주는 맞춤형 추천
- **커뮤니티 자동 생성**  
  - 좋아요 수가 많은 책은 자동으로 팬 커뮤니티가 열려 사용자 간 활발한 소통 가능
- **마이페이지 개인화 기능**  
  - 내가 읽은 책, 대표 도서 설정, 장르별 선호도 시각화 등 개인 독서 프로필 관리
- **AI 확장 기능**  
  - TTS(줄거리 음성 읽기), GPT 기반 리포트 생성, 관련 영화·음악·장소 추천 등 **한 권의 책에서 파생되는 다차원 경험 제공**


---

## 📆 프로젝트 기간
2025.05.22 ~ 2025.05.27 (6일)

---

## 👥 팀원 정보 및 업무 분담

<table style="width:100%; border-collapse:collapse; text-align:center;">
  <tr>
    <th style="width:50%; border:1px solid #e5e7eb; padding:10px;">지현 (Frontend · Backend)</th>
    <th style="width:50%; border:1px solid #e5e7eb; padding:10px;">혜진 (Frontend · Backend)</th>
  </tr>
  <tr>
    <td style="border:1px solid #e5e7eb; padding:10px; text-align:left;">
      - 회원가입 / 로그아웃 기능 개발 <br>
      - 마이페이지 구현 (대표 도서 설정, 읽은 책 분석 등) <br>
      - 메인페이지 구성 <br>
      - 스레드 기능 일부 <br>
      - AI 기반 영화 추천 기능 <br>
      - AI 기반 음악 추천 기능 <br>
      - AI 레포트 기능 및 저장
    </td>
    <td style="border:1px solid #e5e7eb; padding:10px; text-align:left;">
      - 로그인 기능 개발 <br>
      - 도서 목록 페이지 구현 (도서 상세, 좋아요 등 포함) <br>
      - 스레드 기능 일부 <br>
      - 메인페이지 구성 <br>
      - 커뮤니티 기능 개발 (생성 / 조회 / 댓글) <br>
      - AI 기반 장소 추천 기능 <br>
      - AI 기반 도서 추천 기능 <br>
      - AI 레포트 기능 및 저장
    </td>
  </tr>
</table>


---

## 🎯 목표 서비스
- 사용자가 원하는 **분위기/느낌 기반 AI 도서 추천 서비스** 제공
- 책을 중심으로 한 **소셜 커뮤니티 활성화**
- **AI 리포트**를 통한 책·영화·음악·장소 등의 **확장된 문화 경험** 제공
- 독서 기록, 대표 도서, 장르별 통계를 통해 **개인화된 독서 데이터 관리**
- **오디오 기능**으로 독서 경험의 편의성 강화

---

## ⚙️ 구현 정도
- ✅ **AI 추천** : 분위기 기반 도서 추천 (정확도 순으로 3권)
- ✅ **커뮤니티** : 좋아요 수 기반 자동 생성, 스레드 작성/정렬 기능
- ✅ **마이페이지** : 서제 담기, 대표 도서 설정, 장르별 통계
- ✅ **오디오 기능** : gTTS 기반 도서 줄거리 음성 변환 및 재생
- ✅ **AI 리포트** :
  - GPT 기반 줄거리 요약
  - 중요 장소 지도 핀 & 설명
  - 관련 음악 5곡 추천
  - 관련 영화 3편 추천 + 예고편 YouTube 링크
  - 비슷한 도서 3권 추천
  - 리포트 저장 및 PDF 다운로드
- ⏳ **확장 가능성** :
  - 사용자 기반 추천 고도화 (협업 필터링 등)
  - 커뮤니티 내 이벤트 기능 확장
  - 리포트 공유 기능


---

## 🗄️ 데이터베이스 모델링

![books.png](./img/books.png)

---


<!-- ====================== -->
<!-- ⚙️ Backend (Django/DRF) -->
<!-- ====================== -->
<h2>⚙️ Backend</h2>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/DRF-a30000?style=for-the-badge&logo=django&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/CORS%20Headers-0EA5E9?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Pillow-6A5ACD?style=for-the-badge&logo=pillow&logoColor=white" />
  <img src="https://img.shields.io/badge/gTTS-10B981?style=for-the-badge" />
  <img src="https://img.shields.io/badge/OpenAI%20SDK-412991?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/pydantic-4B5563?style=for-the-badge" />
  <img src="https://img.shields.io/badge/httpx-111827?style=for-the-badge" />
</p>

<div align="center">
<table style="width:85%; border-collapse:collapse; margin-top:14px;">
  <thead>
    <tr>
      <th style="background:#10b981;color:#fff;padding:10px;text-align:center;border:1px solid #e5e7eb;">Category</th>
      <th style="background:#10b981;color:#fff;padding:10px;text-align:center;border:1px solid #e5e7eb;">Stack</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Language / Runtime</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">Python 3.11</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Web Framework</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">Django 4.2.5, Django REST Framework 3.16.0</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>CORS / API Client</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">django-cors-headers 4.7.0, httpx 0.28.1, requests 2.32.3</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Media / Utils</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">Pillow 10.0.1, gTTS 2.5.4, Wikipedia-API 0.8.1</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>AI / Validation</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">OpenAI SDK 1.12.0, pydantic 2.10.6</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Infra</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">asgiref 3.7.2, anyio 4.8.0, tzdata 2023.3</td></tr>
  </tbody>
</table>
</div>


<!-- ========================= -->
<!-- 🎨 Frontend (Vue 3 + Vite) -->
<!-- ========================= -->
<h2>🎨 Frontend</h2>

<!-- Centered badges (버전 X) -->
<p align="center">
  <img src="https://img.shields.io/badge/Vue-42B883?style=for-the-badge&logo=vue.js&logoColor=white" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
  <img src="https://img.shields.io/badge/Pinia-F7DF1E?style=for-the-badge&logo=pinia&logoColor=000" />
  <img src="https://img.shields.io/badge/Vue%20Router-CA4245?style=for-the-badge&logo=vue.js&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" />
  <img src="https://img.shields.io/badge/axios-5A29E4?style=for-the-badge" />
  <img src="https://img.shields.io/badge/html2canvas-0F766E?style=for-the-badge" />
  <img src="https://img.shields.io/badge/html--to--image-059669?style=for-the-badge" />
  <img src="https://img.shields.io/badge/jsPDF-CC0000?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Vue%20Toast%20Notification-4B5563?style=for-the-badge" />
</p>

<!-- Table (버전 O) -->
<div align="center">
<table style="width:85%; border-collapse:collapse; margin-top:14px;">
  <thead>
    <tr>
      <th style="background:#0ea5e9;color:#fff;padding:10px 12px;text-align:center;border:1px solid #e5e7eb;">Category</th>
      <th style="background:#0ea5e9;color:#fff;padding:10px 12px;text-align:center;border:1px solid #e5e7eb;">Stack</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Language</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">JavaScript (ESNext)</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Runtime / Build</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">Vite 6.2.4</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Framework</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">Vue 3.5.13, Vue Router 4.5.0, Pinia 3.0.2</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>UI / Styling</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">Bootstrap 5.3.6, Bootstrap-Vue 2.23.1</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Networking</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">axios 1.9.0</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Export / Util</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">html2canvas 1.4.1, html-to-image 1.11.13, jsPDF 3.0.1</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>UX Add-ons</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">vue-toast-notification 3.1.3</td></tr>
  </tbody>
</table>
</div>


<!-- ========================= -->
<!-- 🔧 Versioning / Docs -->
<!-- ========================= -->
<h2>🔧 Versioning</h2>

<p align="center">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white" />
</p>

<div align="center">
<table style="width:75%; border-collapse:collapse; margin-top:14px;">
  <thead>
    <tr>
      <th style="background:#f97316;color:#fff;padding:10px;text-align:center;border:1px solid #e5e7eb;">Category</th>
      <th style="background:#f97316;color:#fff;padding:10px;text-align:center;border:1px solid #e5e7eb;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Git</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">브랜치 전략 / PR 리뷰 / 태깅 / 릴리즈</td></tr>
    <tr><td style="background:#f8fafc;padding:10px;border:1px solid #e5e7eb;"><strong>Notion</strong></td><td style="padding:10px;border:1px solid #e5e7eb;">요구사항 / 기능 명세 / 회의록 / 스프린트 관리</td></tr>
  </tbody>
</table>
</div>


---

### 🤖 도서 추천 알고리즘 기술 설명

본 프로젝트의 도서 추천 알고리즘은 단순한 키워드 매칭을 넘어, **GPT 기반 자연어 이해와 데이터셋 필터링을 결합**하여 설계되었습니다.  

추천 과정은 다음과 같습니다:
1. **사용자 입력 데이터 수집**  
   - 사용자가 현재 열람 중인 도서의 **제목, 작가, 줄거리 요약**을 입력으로 활용합니다.  
   - 이는 단순히 책 제목만으로 추천하는 기존 방식보다 **맥락을 이해한 추천**을 가능하게 합니다.  

2. **전체 도서 데이터셋(books.json) 활용**  
   - 서비스 내에서 제공 가능한 모든 도서 목록을 `books.json` 파일에 구조화하여 관리합니다.  
   - GPT 모델은 프롬프트를 통해 "이 책을 좋아하는 사용자가 선호할 만한 도서를 추천해줘. 단, 추천 결과는 아래 리스트에 포함된 도서 중에서만 골라줘."라는 지시를 받습니다.  
   - 이 과정을 통해 모델은 **외부 데이터에 의존하지 않고**, 반드시 내부 데이터셋에서만 추천 결과를 생성합니다.  

3. **추천 결과 생성**  
   - GPT는 도서의 **주제, 분위기, 문체적 특성** 등을 분석하여 유사성이 높은 장소, 음악, 영화, 책을 추천합니다.  
   - 단순한 키워드 일치가 아닌 **의미 기반의 연관성**을 반영하기 때문에, 사용자의 취향을 더 정밀하게 반영할 수 있습니다.  

4. **정확성과 실효성 확보**  
   - 추천된 결과는 항상 `books.json` 내부의 데이터에 한정되므로, **존재하지 않는 도서가 반환되는 문제를 예방**합니다.  
   - 이를 통해 실제 서비스에서 사용자가 바로 확인하고 읽을 수 있는 도서만 추천되어 **실효성이 높습니다.**  


📌 **기술적 의의**  
- GPT의 **자연어 이해 능력**과 내부 데이터셋을 결합하여 **안정성(존재 보장)**과 **개인화(맥락 반영)**를 동시에 확보  
- 단순 필터링 추천(genre, keyword)보다 **사용자 경험을 고려한 지능형 추천** 구현  
- 확장 가능: 데이터셋이 늘어날 경우에도 동일한 방식으로 추천 품질을 유지할 수 있음  



---

## ⚙️ 핵심 기능 설명

## 📲 기능 구성

<a name="skills"></a>

<div align="center">

<table>
  <tbody align="center"> 
    <tr> <th style="text-align: center"> 메인화면 </th> <th style="text-align: center"> 도서 목록 </th> </tr>
    <tr> <td width="50%"><img width="100%" src="https://github.com/user-attachments/assets/3aa4d90f-6872-4325-89f4-46dde38fff97"/></td> 
        <td width="50%"><img width="100%" src="https://github.com/user-attachments/assets/d47cc697-3f08-4648-8dca-cd3839fd4ac3"/></td> </tr> </tbody>
  <tbody align="center"> 
    <tr> <th style="text-align: center"> 로그인 </th> <th style="text-align: center"> 회원가입 </th> </tr>
    <tr> <td width="50%"><img width="100%" src="https://github.com/user-attachments/assets/532b1838-ce95-425e-93ef-ebf5cdd7291f"/></td>
    <td width="50%"><img width="100%" src="https://github.com/user-attachments/assets/fd3e5761-ec7c-4f7e-9d90-3b0a24c43b93"/></td> </tr> </tbody>
  <tbody align="center"> 
    <tr> <th style="text-align: center"> 도서 상세 및 오디오 읽어주기 생성</th> <th style="text-align: center"> 스레드 작성 </th> </tr>
    <tr> <td width="50%"><img width="100%" src="https://github.com/user-attachments/assets/ae68c35a-ce03-4d0c-8703-4282d59c67e0"/></td>
    <td width="50%"><img width="100%" src="https://github.com/user-attachments/assets/79678d82-5ba5-45c6-a53d-2403d8a295e4"/></td> </tr>
  </tbody>
  <tbody align="center"> 
    <tr> <th style="text-align: center"> 커뮤니티 </th> <th style="text-align: center">  커뮤니티 상세 </th> </tr>
    <tr> <td width="50%"><img width="100%" src="https://github.com/user-attachments/assets/9517d8fd-17a1-4310-a204-072ff160fa82"/></td>
    <td width="50%"><img width="100%" src="https://github.com/user-attachments/assets/1c75092a-f944-4b7a-a216-d4602dc079cd"/></td> </tr>
  </tbody>
  <tbody align="center"> 
    <tr> <th style="text-align: center"> 내 서제에 담기 </th> <th style="text-align: center"> 대표 도서 설정 </th> </tr>
    <tr> <td width="50%"><img width="100%" src="https://github.com/user-attachments/assets/5eb87f22-4372-4079-9b0d-e24f95783418"/></td>
    <td width="50%"><img width="100%" src="https://github.com/user-attachments/assets/c2bc115b-f667-4eda-b47a-d35c3ffaa326"/></td> </tr>
  </tbody>
  <tbody align="center"> 
    <tr> <th style="text-align: center"> AI 리포트 </th> <th style="text-align: center">  AI 리포트 pdf 저장 </th> </tr>
    <tr> <td width="50%"><img width="100%" src="./readme-assets/demostration/live_room_common_user.gif"/></td>
    <td width="50%"><img width="100%" src="./readme-assets/demostration/live_room_lip_reading_user.gif"/></td> </tr>
  </tbody>
</table>
</div>
<br>

---

## 🖥️ 주요 기능

## 📚 기본 도서 기능
- 도서 목록 조회 / 상세보기
- 책 좋아요 및 좋아요 수 기반 커뮤니티 자동 생성
- 댓글 작성 기능 (책마다 댓글 달기 가능)
- 장르 기반 필터링 및 추천
- CRUD 기능 지원:
  - 회원가입 / 로그인 / 로그아웃
  - 마이페이지에서 사용자 데이터 관리
  - 대표 도서 설정 및 변경
  - 읽은 책 체크 기능
  - 댓글 삭제 / 수정



## 👥 커뮤니티 기능
- 좋아요 **100개 이상** 달린 도서 기준으로 자동 생성
- 말머리 기반 자유 게시판 형식 (잡담, 나눔 등 카테고리화 가능)
- 댓글/스레드 기능 (책마다 스레드 작성 가능, 최신순/좋아요순 정렬)
- 사용자 간 피드백 가능 (좋아요, 댓글 등 상호작용 강화)


## 🤖 AI 기능
- **AI 기반 도서 추천**
  - 현재 보고 있는 책 기반으로 GPT가 **유사 도서 3권 추천**
- **AI 감성 기반 추천**
  - “이런 느낌의 책이 읽고 싶다” → GPT가 분석 후 **정확도 순으로 3권 추천**
- **AI 리포트 생성**
  - 사용자가 읽은 책의 줄거리 요약
  - 책 속 중요 장소를 지도에 핀으로 표시 및 이유 설명
  - 관련 음악 5곡 추천
  - 관련 영화 3편 추천 (예고편 YouTube 링크 포함)
  - 비슷한 도서 3권 추천
  - 리포트 저장 및 PDF 다운로드 지원
- **TTS (Text-to-Speech) 기능**
  - 도서 줄거리를 음성으로 읽어주는 기능
- **통합 추천**
  - AI 분석 버튼 클릭 시, **영화 / 음악 / 장소**를 함께 추천


## 🧩 마이페이지 기능
- 내가 담은 책들을 모아 **서제 관리**
- **대표 도서 설정/변경**
- **장르별 통계 시각화** (내가 가장 많이 읽은 장르 확인 가능)
- 내가 생성/저장한 **AI 리포트 탭 제공**
- 저장된 리포트는 **PDF로 다운로드** 가능

---

## 📌 느낀 점 및 후기

### ⚙️ 기술적 경험
- 개발 과정에서 `Client.init() got an unexpected keyword argument 'proxies'` 오류를 경험했는데,  
  `pip install --upgrade openai`를 통해 문제를 해결하면서 **환경 설정 및 패키지 관리의 중요성**을 다시금 체감할 수 있었습니다.  
- Django를 사용하면서 **Django REST Framework 없이도 충분히 RESTful API를 효율적으로 구축할 수 있다**는 점을 직접 경험했습니다.  
  이를 통해 프레임워크의 의존성을 줄이면서도 성능과 확장성을 확보할 수 있는 가능성을 확인했습니다.  
- 로컬 JSON 데이터 파일을 프로젝트 외부에서 관리할 경우 정상 작동하지 않는다는 문제를 겪으며,  
  **데이터 리소스 관리와 프로젝트 구조 설계의 일관성**이 얼마나 중요한지 깨달았습니다.  
- Django의 뷰 템플릿과 백엔드 로직을 동시에 다루며, 실제 서비스 환경에서 발생할 수 있는 다양한 시나리오를 학습할 수 있었고,  
  **프론트엔드와 백엔드의 연결 구조를 직접 체감**할 수 있었습니다.  


### 🤝 협업 및 개발 과정
- 프로젝트를 진행하며 **팀원 간 역할 분담과 원활한 커뮤니케이션의 중요성**을 깊이 느꼈습니다.  
- 작은 기능 하나라도 프론트엔드와 백엔드가 긴밀히 연결되어 있어, 사소한 변경 사항도 즉시 공유하고 테스트하는 과정이 필수적이었습니다.  
- 기능 구현뿐만 아니라 **테스트·디버깅·코드 리뷰 과정에서의 협력**이 프로젝트 품질을 높이는 핵심이라는 점을 경험했습니다.   
- 이번 프로젝트는 단순한 학습을 넘어 실제 서비스 구현에 가까운 과정을 경험할 수 있었으며,  
  협업 툴과 워크플로우를 적극적으로 활용하면서 **실무형 협업 프로세스**에 한 걸음 더 다가갈 수 있었습니다.  


---

### ✨ 기타 및 자유 작성

본 프로젝트는 단순한 도서 추천 서비스에서 그치지 않고, **AI 기반 감성 분석과 콘텐츠 확장 추천**이라는 실험적인 도전을 통해 새로운 사용자 경험을 창출할 수 있었습니다.  
특히 책을 중심으로 음악, 영화, 장소 등 **이종(異種) 콘텐츠를 연계 추천**하는 기능을 직접 구현하면서,  
한 권의 책이 단순한 읽을거리에서 **문화적 경험의 허브**로 확장될 수 있음을 보여주었습니다.  

또한 "이런 분위기의 책을 읽고 싶다"라는 **감성 기반 자연어 요청을 분석**하여, 사용자 맞춤형 추천 결과를 제공한 점은  
기존의 단순 키워드 기반 추천 시스템과 차별화되는 중요한 성과였습니다.  

향후 발전 방향으로는 다음과 같은 부분을 고려할 수 있습니다:
- 📊 **사용자 피드백 기반 추천 보정**: 추천 결과에 대한 사용자의 만족도를 반영하여 모델 학습 및 결과 품질 개선  
- 🎯 **추천 정확도 고도화**: 대규모 도서 데이터셋 학습과 최신 언어모델 적용을 통한 정밀한 매칭  
- 🌍 **다양한 미디어와의 연동**: 책뿐만 아니라 웹툰, 강연, 다큐멘터리 등 확장 콘텐츠로의 연결  
- ☁️ **실서비스화를 위한 확장**: 클라우드 기반 배포, 실시간 데이터 동기화, 모바일 앱 확장 등을 통해 접근성과 사용성을 강화  

이를 통해 본 프로젝트는 단순한 졸업작품이나 실습 결과를 넘어,  
**지속적인 발전 가능성을 가진 실질적인 서비스 모델**로 확장될 수 있을 것으로 기대됩니다.

