from .model import Model

print('start loads recomendation model..')
Model.load()
art = Model.predict_unpopular_artists(['folkrock'], ['en'])
print(*[s[0].encode('utf-8').decode('utf-8', errors='replace') for s in art])
print('model loaded')
