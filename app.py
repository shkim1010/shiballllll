import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import google.generativeai as genai
from google import genai
from google.genai import types
import firebase_admin
from firebase_admin import credentials, db

# Spotify API 인증
client_id = '1d5d33c00ef244dfae00a6173aa0aece'
client_secret = 'ccb6a44ef9e64837ab83c513d9bb8472'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# 사용자 입력 받기
song_title = input("저기... 우리 저번에 듣던, 노래... ")
singer_name = input("이 부른 거...!")

# Spotify에서 곡 검색
track_results = sp.search(q=f"track:{song_title} artist:{singer_name}", limit=1)
track_info = track_results['tracks']['items'][0]

# 장르 정보가 없는 경우 아티스트의 장르로 대체
track_genre = []
if 'genres' in track_info:
    track_genre = track_info['genres']
else:
    # 아티스트의 장르 정보 가져오기
    artist_id = track_info['artists'][0]['id']
    artist_info = sp.artist(artist_id)
    track_genre = artist_info['genres']

# 곡 정보 출력
track_name = track_info['name']
track_artists = ', '.join([artist['name'] for artist in track_info['artists']])

print(f"곡명: {track_name}")
print(f"아티스트: {track_artists}")
print(f"장르: {track_genre}")

# Gemini API 사용 (향수 추천 받기)
client = genai.Client(api_key='AIzaSyA8vEpyicI6A3C2_urLO-PG7QTpQoT-qMI')

# 향수 추천 정보 설정
top_notes = ["라벤더", "레몬", "자몽", "로즈마리", "페퍼민트"]
middle_notes = ["클린코튼", "라일락", "피오니", "자스민", "일랑일랑"]
base_notes = ["샌달우드", "시더우드", "바닐라", "화이트머스크", "블랙머스크"]

note_info = (
    f"내가 가진 향료는 다음과 같아:\n"
    f"- 탑 노트: {', '.join(top_notes)}\n"
    f"- 미들 노트: {', '.join(middle_notes)}\n"
    f"- 베이스 노트: {', '.join(base_notes)}\n"
    f"이 향료들 중에서 탑, 미들, 베이스 하나씩 추천해줘. 다른 향을 추천하고 싶다면 이 향료랑 비슷한 향을 이 향료들로 대체해야해."
)

# 곡과 관련된 향수 추천
prompt = (
    f"이 노래 '{track_name}'의 장르 {track_genre}에 어울리는 향수를 추천해줘.\n"
    f"{note_info}"
)

response = client.models.generate_content(
  model="gemini-2.0-flash",
  contents=[types.Part(content=prompt)]
)

print("AI 추천 향수:", response.text)

# Firebase 연동
if not firebase_admin._apps:
    cred = credentials.Certificate('bbbb-b2de2-firebase-adminsdk-fbsvc-29fa592319.json')  # Firebase 서비스 계정 키 파일
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://bbbb-b2de2-default-rtdb.firebaseio.com/'  # Firebase Realtime DB URL
    })

# 데이터베이스에 저장할 데이터
fragrance_data = {
    'top': '라벤더',
    'middle': '자스민',
    'base': '샌달우드'
}

# Firebase Realtime Database에 데이터 저장
def save_fragrance_data(song_title, fragrance_data):
    ref = db.reference(f'/fragrance_recommendations/{song_title}')
    ref.set(fragrance_data)

# 데이터 저장
save_fragrance_data(track_name, fragrance_data)
