import vk_api
import vk_audio

token = ''
vk_session = vk_api.VkApi(token=token)

vk = vk_audio.VkAudio(vk=vk_session)

owner = None #Если None - аудио будут браться из своей музыки
data = vk.load(owner)#получаем наши аудио

second_audio = data.Audios[1]#берем вторую аудиозапись
format_string = "{title} - {artist} ({owner_id}_{id}) -> {url}"
print("2.",format_string.format(
    title=second_audio.title, #так же можно second_audio['title']
    artist=second_audio.artist,
    owner_id = second_audio.owner_id,
    id=second_audio.id,
    url=second_audio.url
))