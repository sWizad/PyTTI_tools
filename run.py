#@title #2.1 Parameters:
from os.path import exists as path_exists

try:
  from pytti.Notebook import change_tqdm_color, get_last_file
except ModuleNotFoundError:
  if drive_mounted:
    #THIS IS NOT AN ERROR. This is the code that would
    #make an error if something were wrong.
    raise RuntimeError('ERROR: please run setup (step 1.3).')
  else:
    #THIS IS NOT AN ERROR. This is the code that would
    #make an error if something were wrong.
    raise RuntimeError('WARNING: drive is not mounted.\nERROR: please run setup (step 1.3).')
change_tqdm_color()

import glob, json, random, re, math
try:
  from bunch import Bunch
except ModuleNotFoundError:
  if drive_mounted:
    #THIS IS NOT AN ERROR. This is the code that would
    #make an error if something were wrong.
    raise RuntimeError('ERROR: please run setup (step 1.3).')
  else:
    #THIS IS NOT AN ERROR. This is the code that would
    #make an error if something were wrong.
    raise RuntimeError('WARNING: drive is not mounted.\nERROR: please run setup (step 1.3).')

#these are used to make the defaults look pretty
model_default = None
random_seed = None
all  = math.inf
derive_from_init_aspect_ratio = -1

def define_parameters():
  locals_before = locals().copy()
  #@markdown ###Prompts:
  
  scenes = "deep space habitation ring made of glass | galactic nebula | wow! space is full of fractal creatures darting around everywhere like fireflies"#@param{type:"string"}
  scene_prefix = "astrophotography #pixelart | image credit nasa | space full of cybernetic neon:3_galactic nebula | isometric pixelart by Sachin Teng | "#@param{type:"string"}
  scene_suffix = "| satellite image:-1:-.95 | text:-1:-.95 | anime:-1:-.95 | watermark:-1:-.95 | backyard telescope:-1:-.95 | map:-1:-.95"#@param{type:"string"}
  interpolation_steps = 0#@param{type:"number"}
  steps_per_scene =  60100#@param{type:"raw"}
  #@markdown ---
  #@markdown ###Image Prompts:
  direct_image_prompts   = ""#@param{type:"string"}
  #@markdown ---
  #@markdown ###Initial image:
  init_image = ""#@param{type:"string"}
  direct_init_weight =  ""#@param{type:"string"}
  semantic_init_weight = ""#@param{type:"string"}
  #@markdown ---
  #@markdown ###Image:
  #@markdown Use `image_model` to select how the model will encode the image
  image_model = "Limited Palette" #@param ["VQGAN", "Limited Palette", "Unlimited Palette"]

  #@markdown image_model | description | strengths | weaknesses
  #@markdown --- | -- | -- | --
  #@markdown  VQGAN | classic VQGAN image | smooth images | limited datasets, slow, VRAM intesnsive 
  #@markdown  Limited Palette | pytti differentiable palette | fast,  VRAM scales with `palettes` | pixel images
  #@markdown  Unlimited Palette | simple RGB optimization | fast, VRAM efficient | pixel images
  
  #@markdown The output image resolution will be `width` $\times$ `pixel_size` by height $\times$ `pixel_size` pixels.
  #@markdown The easiest way to run out of VRAM is to select `image_model` VQGAN without reducing
  #@markdown `pixel_size` to $1$.

  #@markdown For `animation_mode: 3D` the minimum resoultion is about 450 by 400 pixels.
  width =  180#@param {type:"raw"}
  height =  112#@param {type:"raw"}
  pixel_size = 4#@param{type:"number"}
  smoothing_weight =  0.02#@param{type:"number"}
  #@markdown `VQGAN` specific settings:
  vqgan_model = "sflckr" #@param ["imagenet", "coco", "wikiart", "sflckr", "openimages"]
  #@markdown `Limited Palette` specific settings:
  random_initial_palette = False#@param{type:"boolean"}
  palette_size = 6#@param{type:"number"}
  palettes   = 9#@param{type:"number"}
  gamma = 1#@param{type:"number"}
  hdr_weight = 0.01#@param{type:"number"}
  palette_normalization_weight = 0.2#@param{type:"number"}
  show_palette = False #@param{type:"boolean"}
  target_palette = ""#@param{type:"string"}
  lock_palette = False #@param{type:"boolean"}
  #@markdown ---
  #@markdown ###Animation:
  animation_mode = "3D" #@param ["off","2D", "3D", "Video Source"]
  sampling_mode = "bicubic" #@param ["bilinear","nearest","bicubic"]
  infill_mode = "wrap" #@param ["mirror","wrap","black","smear"]
  pre_animation_steps =  100#@param{type:"number"}
  steps_per_frame =  50#@param{type:"number"}
  frames_per_second =  12#@param{type:"number"}
  #@markdown ---
  #@markdown ###Stabilization Weights:
  direct_stabilization_weight = ""#@param{type:"string"}
  semantic_stabilization_weight = ""#@param{type:"string"}
  depth_stabilization_weight = ""#@param{type:"string"}
  edge_stabilization_weight = ""#@param{type:"string"}
  #@markdown `flow_stabilization_weight` is used for `animation_mode: 3D` and `Video Source`
  flow_stabilization_weight = ""#@param{type:"string"}
  #@markdown ---
  #@markdown ###Video Tracking:
  #@markdown Only for `animation_mode: Video Source`.
  video_path = ""#@param{type:"string"}
  frame_stride = 1#@param{type:"number"}
  reencode_each_frame = True #@param{type:"boolean"}
  flow_long_term_samples = 1#@param{type:"number"}
  #@markdown ---
  #@markdown ###Image Motion:
  translate_x    = "-1700*sin(radians(1.5))" #@param{type:"string"}
  translate_y    = "0" #@param{type:"string"}
  #@markdown `..._3d` is only used in 3D mode.
  translate_z_3d = "(50+10*t)*sin(t/10*pi)**2" #@param{type:"string"}
  #@markdown `rotate_3d` *must* be a `[w,x,y,z]` rotation (unit) quaternion. Use `rotate_3d: [1,0,0,0]` for no rotation.
  #@markdown [Learn more about rotation quaternions here](https://eater.net/quaternions).
  rotate_3d      = "[cos(radians(1.5)), 0, -sin(radians(1.5))/sqrt(2), sin(radians(1.5))/sqrt(2)]"#@param{type:"string"}
  #@markdown `..._2d` is only used in 2D mode.
  rotate_2d      = "5" #@param{type:"string"}
  zoom_x_2d      = "0" #@param{type:"string"}
  zoom_y_2d      = "0" #@param{type:"string"}
  #@markdown  3D camera (only used in 3D mode):
  lock_camera   = True#@param{type:"boolean"}
  field_of_view = 60#@param{type:"number"}
  near_plane    = 1#@param{type:"number"}
  far_plane     = 10000#@param{type:"number"}

  #@markdown ---
  #@markdown ###Output:
  file_namespace = "default"#@param{type:"string"}
  if file_namespace == '':
    file_namespace = 'out'
  allow_overwrite = False#@param{type:"boolean"}
  base_name = file_namespace
  if not allow_overwrite and path_exists(f'images_out/{file_namespace}'):
    _, i = get_last_file(f'images_out/{file_namespace}', 
                         f'^(?P<pre>{re.escape(file_namespace)}\\(?)(?P<index>\\d*)(?P<post>\\)?_1\\.png)$')
    if i == 0:
      print(f"WARNING: file_namespace {file_namespace} already has images from run 0")
    elif i is not None:
      print(f"WARNING: file_namespace {file_namespace} already has images from runs 0 through {i}")
  elif glob.glob(f'images_out/{file_namespace}/{base_name}_*.png'):
    print(f"WARNING: file_namespace {file_namespace} has images which will be overwritten")
  try:
    del i
    del _
  except NameError:
    pass
  del base_name
  display_every = steps_per_frame #@param{type:"raw"}
  clear_every = 0 #@param{type:"raw"}
  display_scale = 1#@param{type:"number"}
  save_every = steps_per_frame #@param{type:"raw"}
  backups =  2**(flow_long_term_samples+1)+1#this is used for video transfer, so don't lower it if that's what you're doing#@param {type:"raw"}
  show_graphs = False #@param{type:"boolean"}
  approximate_vram_usage = False#@param{type:"boolean"}

  #@markdown ---
  #@markdown ###Model:
  #@markdown Quality settings from Dribnet's CLIPIT (https://github.com/dribnet/clipit).
  #@markdown Selecting too many will use up all your VRAM and slow down the model.
  #@markdown I usually use ViTB32, ViTB16, and RN50 if I get a A100, otherwise I just use ViT32B.

  #@markdown quality | CLIP models
  #@markdown --- | --
  #@markdown  draft | ViTB32 
  #@markdown  normal | ViTB32, ViTB16 
  #@markdown  high | ViTB32, ViTB16, RN50
  #@markdown  best | ViTB32, ViTB16, RN50x4
  ViTB32 = True #@param{type:"boolean"}
  ViTB16 = False #@param{type:"boolean"}
  RN50 = False #@param{type:"boolean"}
  RN50x4 = False #@param{type:"boolean"}
  ViTL14  = False #@param{type:"boolean"}
  RN101 = False #@param{type:"boolean"}
  RN50x16 = False #@param{type:"boolean"}
  RN50x64 = False #@param{type:"boolean"}
  #@markdown the default learning rate is `0.1` for all the VQGAN models
  #@markdown except openimages, which is `0.15`. For the palette modes the
  #@markdown default is `0.02`. 
  learning_rate =  model_default#@param{type:"raw"}
  reset_lr_each_frame = True#@param{type:"boolean"}
  seed = random_seed #@param{type:"raw"}
  #@markdown **Cutouts**:

  #@markdown [Cutouts are how CLIP sees the image.](https://twitter.com/remi_durant/status/1460607677801897990)
  cutouts =  40#@param{type:"number"}
  cut_pow =  2#@param {type:"number"}
  cutout_border =  .25#@param {type:"number"}
  gradient_accumulation_steps = 1 #@param {type:"number"}
  #@markdown NOTE: prompt masks (`promt:weight_[mask.png]`) will not work right on '`wrap`' or '`mirror`' mode.
  border_mode = "clamp" #@param ["clamp","mirror","wrap","black","smear"]
  models_parent_dir = '.'
  
  if seed is None:
    seed = random.randint(-0x8000_0000_0000_0000, 0xffff_ffff_ffff_ffff)
  locals_after = locals().copy()
  for k in locals_before.keys():
    del locals_after[k]
  del locals_after['locals_before']
  return locals_after

params = Bunch(define_parameters())
print("SETTINGS:")
print(json.dumps(params))


from pytti.workhorse import _main as render_frames
from omegaconf import OmegaConf
cfg = OmegaConf.create(dict(params))

# function wraps step 2.3 of the original p5 notebook
render_frames(cfg)