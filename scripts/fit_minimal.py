import struct, zipfile, tempfile, os, json, math
from datetime import datetime, timezone, timedelta
from pathlib import Path

FIT_EPOCH = datetime(1989,12,31,tzinfo=timezone.utc)
BASE_TYPES={0x00:('enum','B',1),0x01:('sint8','b',1),0x02:('uint8','B',1),0x03:('sint16','h',2),0x04:('uint16','H',2),0x05:('sint32','i',4),0x06:('uint32','I',4),0x07:('string',None,1),0x08:('float32','f',4),0x09:('float64','d',8),0x0a:('uint8z','B',1),0x0b:('uint16z','H',2),0x0c:('uint32z','I',4),0x0d:('byte','B',1),0x0e:('sint64','q',8),0x0f:('uint64','Q',8),0x10:('uint64z','Q',8)}
INVALID={'enum':0xFF,'sint8':0x7F,'uint8':0xFF,'sint16':0x7FFF,'uint16':0xFFFF,'sint32':0x7FFFFFFF,'uint32':0xFFFFFFFF,'float32':None,'float64':None,'uint8z':0,'uint16z':0,'uint32z':0,'byte':0xFF,'sint64':0x7FFFFFFFFFFFFFFF,'uint64':0xFFFFFFFFFFFFFFFF,'uint64z':0}
FIELD_NAMES={
18:{253:'timestamp',0:'event',1:'event_type',2:'start_time',3:'start_position_lat',4:'start_position_long',5:'sport',6:'sub_sport',7:'total_elapsed_time',8:'total_timer_time',9:'total_distance',10:'total_cycles',11:'total_calories',14:'avg_speed',15:'max_speed',16:'avg_heart_rate',17:'max_heart_rate',18:'avg_cadence',19:'max_cadence',20:'avg_power',21:'max_power',22:'total_ascent',23:'total_descent',24:'total_training_effect',25:'first_lap_index',26:'num_laps',34:'num_active_lengths',39:'total_work',65:'enhanced_avg_speed',66:'enhanced_max_speed',67:'enhanced_avg_altitude',68:'enhanced_min_altitude',69:'enhanced_max_altitude',110:'total_anaerobic_training_effect'},
20:{253:'timestamp',0:'position_lat',1:'position_long',2:'altitude',3:'heart_rate',4:'cadence',5:'distance',6:'speed',7:'power',9:'grade',13:'temperature',16:'left_right_balance',29:'accumulated_power',30:'vertical_speed',31:'calories',32:'vertical_oscillation',33:'stance_time_percent',34:'stance_time',39:'vertical_ratio',40:'stance_time_balance',41:'step_length',42:'cycle_length',43:'absolute_pressure',44:'depth',45:'next_stop_depth',46:'next_stop_time',47:'time_to_surface',48:'ndl_time',49:'cns_load',50:'n2_load',52:'enhanced_speed',73:'enhanced_altitude'},
19:{253:'timestamp',2:'start_time',3:'start_position_lat',4:'start_position_long',5:'end_position_lat',6:'end_position_long',7:'total_elapsed_time',8:'total_timer_time',9:'total_distance',10:'total_cycles',11:'total_calories',12:'total_fat_calories',13:'avg_speed',14:'max_speed',15:'avg_heart_rate',16:'max_heart_rate',17:'avg_cadence',18:'max_cadence',19:'avg_power',20:'max_power',21:'total_ascent',22:'total_descent',32:'sport',33:'event_group',71:'enhanced_avg_speed',72:'enhanced_max_speed'},
0:{0:'type',1:'manufacturer',2:'product',3:'serial_number',4:'time_created'},
34:{253:'timestamp',0:'total_timer_time',1:'num_sessions',2:'type',3:'event',4:'event_type',5:'local_timestamp'},
4:{253:'timestamp',0:'name',1:'sport',2:'sub_sport',3:'pool_length',4:'pool_length_unit'}
}
SCALE_OFFSET={'altitude':(5,500),'enhanced_altitude':(5,500),'enhanced_avg_altitude':(5,500),'enhanced_min_altitude':(5,500),'enhanced_max_altitude':(5,500),'distance':(100,0),'total_distance':(100,0),'speed':(1000,0),'avg_speed':(1000,0),'max_speed':(1000,0),'enhanced_speed':(1000,0),'enhanced_avg_speed':(1000,0),'enhanced_max_speed':(1000,0),'total_elapsed_time':(1000,0),'total_timer_time':(1000,0),'total_training_effect':(10,0),'total_anaerobic_training_effect':(10,0),'grade':(100,0),'vertical_oscillation':(10,0),'stance_time_percent':(100,0),'stance_time':(10,0),'vertical_ratio':(100,0),'stance_time_balance':(100,0),'step_length':(10,0)}
SPORTS={0:'Generic',1:'Running',2:'Cycling',3:'Transition',4:'Fitness Equipment',5:'Swimming',6:'Basketball',7:'Soccer',8:'Tennis',9:'American Football',10:'Training',11:'Walking',12:'Cross Country Skiing',13:'Alpine Skiing',14:'Snowboarding',15:'Rowing',16:'Mountaineering',17:'Hiking',18:'Multisport',19:'Paddling',20:'Flying',21:'E-Biking',22:'Motorcycling',23:'Boating',24:'Driving',25:'Golf',26:'Hang Gliding',27:'Horseback Riding',28:'Hunting',29:'Fishing',30:'Inline Skating',31:'Rock Climbing',32:'Sailing',33:'Ice Skating',34:'Sky Diving',35:'Snowshoeing',36:'Snowmobiling',37:'Stand Up Paddleboarding',38:'Surfing',39:'Wakeboarding',40:'Water Skiing',41:'Kayaking',42:'Rafting',43:'Windsurfing',44:'Kitesurfing',45:'Tactical',46:'Jumpmaster',47:'Boxing',48:'Floor Climbing',53:'All',54:'Diving',55:'HIIT',56:'Racket',57:'Wheelchair Push Walk',58:'Wheelchair Push Run',59:'Meditation',60:'Disc Golf',61:'Generic Fitness',62:'Obstacle',63:'Breathing',64:'Generic Running',65:'Generic Cycling',66:'Generic Swimming',67:'Generic Walking',68:'Generic Hiking'}

def ts(v):
 try: return FIT_EPOCH+timedelta(seconds=int(v))
 except: return None

def semi(v): return float(v)*(180.0/2**31) if v is not None else None

def read_value(raw, base_type, endian):
 t=base_type&0x1F; name,fmt,size=BASE_TYPES.get(t,('unknown',None,1))
 if name=='string': return raw.split(b'\0',1)[0].decode('utf-8','ignore')
 if fmt is None: return raw
 count=len(raw)//size
 try: vals=struct.unpack(endian+(fmt*count), raw[:count*size])
 except Exception: return None
 inv=INVALID.get(name)
 def vv(x): return None if (inv is not None and x==inv) else x
 return vv(vals[0]) if count==1 else [vv(x) for x in vals]

def units(name,val):
 if val is None: return None
 if name in ('timestamp','start_time','time_created'): return ts(val)
 if name in ('position_lat','position_long','start_position_lat','start_position_long','end_position_lat','end_position_long'): return semi(val)
 if isinstance(val,(int,float)) and name in SCALE_OFFSET:
  sc,off=SCALE_OFFSET[name]; return val/sc-off
 return val

def parse_fit_bytes(data):
 header_size=data[0]
 if data[8:12]!=b'.FIT': raise ValueError('missing .FIT')
 data_size=struct.unpack_from('<I',data,4)[0]
 i=header_size; end=i+data_size; defs={}; messages=[]; last_ts=None
 while i<end:
  header=data[i]; i+=1
  if header & 0x80:
   local_type=(header>>5)&0x03; time_offset=header&0x1F; d=defs.get(local_type)
   if not d: continue
   if last_ts is not None: last_ts=(last_ts&~0x1F)+time_offset
   else: last_ts=time_offset
   global_num=d['global_num']; values={}
   for field in d['fields']:
    raw=data[i:i+field['size']]; i+=field['size']
    name=FIELD_NAMES.get(global_num,{}).get(field['num'],f'field_{field["num"]}')
    values[name]=units(name,read_value(raw,field['base_type'],d['endian']))
   # SKIP developer field bytes
   for dev in d.get('dev_fields',[]):
    i += dev['size']
   if 'timestamp' not in values and last_ts is not None: values['timestamp']=ts(last_ts)
   messages.append({'global':global_num,**values})
   continue
  is_def=bool(header&0x40); local_type=header&0x0f
  if is_def:
   reserved=data[i]; arch=data[i+1]; i+=2; endian='>' if arch==1 else '<'
   global_num=struct.unpack_from(endian+'H',data,i)[0]; i+=2
   n=data[i]; i+=1; fields=[]
   for _ in range(n):
    num,size,base_type=data[i],data[i+1],data[i+2]; i+=3
    fields.append({'num':num,'size':size,'base_type':base_type})
   dev_fields=[]
   if header&0x20:
    nd=data[i]; i+=1
    for _ in range(nd):
     num,size,dev_idx=data[i],data[i+1],data[i+2]; i+=3
     dev_fields.append({'num':num,'size':size,'dev_idx':dev_idx})
   defs[local_type]={'global_num':global_num,'fields':fields,'dev_fields':dev_fields,'endian':endian}
  else:
   d=defs.get(local_type)
   if not d:
    #print('missing def at',i,local_type); break
    raise ValueError('missing def')
   global_num=d['global_num']; values={}
   for field in d['fields']:
    raw=data[i:i+field['size']]; i+=field['size']
    name=FIELD_NAMES.get(global_num,{}).get(field['num'],f'field_{field["num"]}')
    values[name]=units(name,read_value(raw,field['base_type'],d['endian']))
   for dev in d.get('dev_fields',[]):
    i += dev['size']
   if isinstance(values.get('timestamp'),datetime): last_ts=int((values['timestamp']-FIT_EPOCH).total_seconds())
   messages.append({'global':global_num,**values})
 return messages

def parse(path):
 return parse_fit_bytes(open(path,'rb').read())

if __name__=='__main__':
 z='/mnt/data/exportSportData_466571768635605001_20260518.zip'
 tmp='/mnt/data/coros_fit2'; Path(tmp).mkdir(exist_ok=True)
 with zipfile.ZipFile(z) as zz:
  if not list(Path(tmp).glob('*.fit')):
   zz.extractall(tmp)
 files=list(Path(tmp).glob('*.fit'))
 sessions=[]; fail=[]
 for p in files:
  try:
   msgs=parse(str(p))
   ss=[m for m in msgs if m.get('global')==18]
   if ss:
    for s in ss:
     s['file']=p.name; sessions.append(s)
  except Exception as e:
   fail.append((p.name,str(e)))
 from collections import Counter
 print('files',len(files),'sessions',len(sessions),'fail',len(fail))
 print('sports raw', Counter(s.get('sport') for s in sessions))
 print('sports named', Counter(SPORTS.get(s.get('sport'),s.get('sport')) for s in sessions))
 print('dist max', max((s.get('total_distance') or 0 for s in sessions), default=0))
 top=sorted(sessions, key=lambda s:s.get('total_distance') or 0, reverse=True)[:10]
 for s in top:
  print(s['file'], SPORTS.get(s.get('sport'),s.get('sport')), s.get('sub_sport'), s.get('start_time'), s.get('total_distance'), s.get('total_timer_time'), s.get('avg_heart_rate'))
 print('date range', min([s.get('start_time') for s in sessions if s.get('start_time')]), max([s.get('start_time') for s in sessions if s.get('start_time')]))
