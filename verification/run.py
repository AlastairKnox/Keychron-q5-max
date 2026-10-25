from pathlib import Path
import re,subprocess,sys
here=Path(__file__).resolve().parent
qmk_root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else here.parent/'qmk-keychron'
keymap=qmk_root/'keyboards/keychron/q5_max/ansi_encoder/keymaps/alastair/keymap.c'
source=keymap.read_text()+(keymap.parent/'select_word.c').read_text()
# Check actual layout positions against the board's matrix definition.
import json
maps={name:[k.strip() for k in body.split(',')] for name,body in re.findall(r'\[(\w+)\] = LAYOUT_ansi_101\((.*?)\),\n',keymap.read_text(),re.S)}
positions=json.loads((qmk_root/'keyboards/keychron/q5_max/ansi_encoder/keyboard.json').read_text())['layouts']['LAYOUT_ansi_101']['layout']
fn={tuple(p['matrix']):k for p,k in zip(positions,maps['LINUX_FN'])}
assert fn[2,10]=='PROCESS_LIST' and fn[3,6]=='SHELL_HISTORY' and fn[3,7]=='_______' and fn[5,16]=='LNX_CALC' and fn[2,9]=='DM_PLY1'
assert fn[tuple(positions[maps['LINUX_BASE'].index('KC_H')]['matrix'])]=='SHELL_HISTORY'
assert maps['LINUX_BASE'][next(i for i,p in enumerate(positions) if p['matrix']==[5,16])]=='KC_P0'
keys=set(re.findall(r'\b(?:KC_[A-Z0-9_]+|UG_[A-Z0-9_]+|MS_[A-Z0-9_]+|BT_HST[123]|P2P4G|BAT_LVL|SC_LSPO|SC_RSPC|CW_TOGG|DM_REC1|DM_RSTP|DM_PLY1)\b',source))
mods=['KC_LCTL','KC_LSFT','KC_LALT','KC_LGUI','KC_RCTL','KC_RSFT','KC_RALT','KC_RGUI']
keys-=set(mods+['KC_LEFT_SHIFT','KC_TRNS'])
header='''#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include <assert.h>
#define VIA_ENABLE
#define PROGMEM
#define MATRIX_ROWS 1
#define MATRIX_COLS 114
#define NUM_ENCODERS 1
#define NUM_DIRECTIONS 2
#define NO_LED 255
#define SAFE_RANGE 0x7e00
#define KC_TRNS 1
#define _______ KC_TRNS
#define LAYOUT_ansi_101(...) {{__VA_ARGS__}}
#define ENCODER_CCW_CW(a,b) {a,b}
#define MO(l) (0x5200+(l))
#define LCTL(k) ((k)|0x0100)
#define LSFT(k) ((k)|0x0200)
#define LALT(k) ((k)|0x0400)
#define LGUI(k) ((k)|0x0800)
#define MOD_MASK_SHIFT 0x22
#define MOD_MASK_CTRL 0x11
#define MOD_BIT(k) (1U<<((k)-224))
#define MOD_LSFT 2
#define RGB_MATRIX_TYPING_HEATMAP 42
#define KC_LEFT_SHIFT KC_LSFT
typedef uint32_t layer_state_t;
layer_state_t default_layer_state_set_user(layer_state_t state);
typedef struct { uint8_t col,row; } keypos_t;
typedef struct { struct { bool pressed; uint16_t time; keypos_t key; } event; } keyrecord_t;
typedef struct { uint8_t matrix_co[MATRIX_ROWS][MATRIX_COLS]; } led_config_t;
typedef struct { uint8_t trigger_mods; uint16_t trigger,replacement; uint32_t layers; } key_override_t;
#define ko_make_with_layers(m,k,r,l) {m,k,r,l}
static struct { bool autocorrect_enable; } keymap_config;
static led_config_t g_led_config;
static uint32_t default_layer_state=1,layer_state;
static uint8_t held_mods,weak_mods,oneshot,rgb_mode=7;
static uint8_t led_red,led_green,led_blue;
typedef struct { bool caps_lock; } led_t;
static led_t host_keyboard_led_state(void){return (led_t){0};}
static int autocorrect_resets,default_handler_calls,caps_resets,taps;
static uint16_t last_tap;
static char literal[256];
static uint16_t stored_square, stored_fn_l=KC_TRNS;
static uint16_t stored_extra[6][19];
static uint16_t dynamic_keymap_get_keycode(uint8_t l,uint8_t r,uint8_t c){if(l==5&&r==3&&c==9)return stored_fn_l;if(l==4&&r==0&&c==17)return stored_square;return stored_extra[r][c];}
static void dynamic_keymap_set_keycode(uint8_t l,uint8_t r,uint8_t c,uint16_t k){if(l==5&&r==3&&c==9){stored_fn_l=k;return;}if(l==4&&r==0&&c==17){stored_square=k;return;}stored_extra[r][c]=k;}
static uint8_t get_mods(void){return held_mods;}
static uint8_t get_weak_mods(void){return weak_mods;}
static uint8_t get_oneshot_mods(void){return oneshot;}
static void set_mods(uint8_t m){held_mods=m;}
static void set_weak_mods(uint8_t m){weak_mods=m;}
static void set_oneshot_mods(uint8_t m){oneshot=m;}
static void clear_mods(void){held_mods=0;}
static void clear_weak_mods(void){weak_mods=0;}
static void clear_oneshot_mods(void){oneshot=0;}
static void register_mods(uint8_t m){held_mods|=m;}
static void unregister_mods(uint8_t m){held_mods&=~m;}
static void send_keyboard_report(void){}
static void tap_code(uint16_t k){last_tap=k; taps++;}
static void tap_code16(uint16_t k){tap_code(k);}
static void register_code(uint16_t k){if(k>=224&&k<=231)held_mods|=1U<<(k-224);tap_code(k);}
static void unregister_code(uint16_t k){if(k>=224&&k<=231)held_mods&=~(1U<<(k-224));}
static void clear_keyboard(void){held_mods=weak_mods=oneshot=0;}
static void layer_clear(void){layer_state=0;}
static void layer_state_set(layer_state_t s){layer_state=s;}
static bool layer_state_is(uint8_t l){return (layer_state&(1UL<<l))!=0;}
static void default_layer_set(uint32_t l){default_layer_state=default_layer_state_set_user(l);}
static uint8_t get_highest_layer(uint32_t l){uint8_t n=0;while(l>>=1)n++;return n;}
static void caps_word_off(void){caps_resets++;}
static uint8_t rgb_matrix_get_mode(void){return rgb_mode;}
static void rgb_matrix_mode_noeeprom(uint8_t m){rgb_mode=m;}
static void rgb_matrix_set_color(uint8_t i,uint8_t r,uint8_t g,uint8_t b){if(!i){led_red=r;led_green=g;led_blue=b;}}
static uint16_t keymap_key_to_keycode(uint8_t l,keypos_t k){return KC_TRNS;}
static void send_string(const char *s){assert(!held_mods&&!weak_mods&&!oneshot);strcpy(literal,s);}
static bool process_autocorrect(uint16_t k,keyrecord_t *r){autocorrect_resets++;return true;}
static bool process_autocorrect_default_handler(uint16_t *k,keyrecord_t *r,uint8_t *b,uint8_t *m){default_handler_calls++;return true;}
bool dynamic_macro_record_end_user(int8_t direction);
void dynamic_macro_stop_recording(void);
bool process_dynamic_macro(uint16_t keycode, keyrecord_t *record);
void process_record(keyrecord_t *record);
#define DYNAMIC_MACRO_SIZE 256
#define DYNAMIC_MACRO_NO_NESTING
#define dprintln(...) ((void)0)
#define dprintf(...) ((void)0)
'''
header+='\n'.join(f'#define {k} {i+2}' for i,k in enumerate(sorted(keys)))+'\n'
header+='\n'.join(f'#define {k} {i+224}' for i,k in enumerate(mods))+'\n'
header+='''
#define QK_DYNAMIC_MACRO_RECORD_START_1 DM_REC1
#define QK_DYNAMIC_MACRO_RECORD_START_2 0x7101
#define QK_DYNAMIC_MACRO_PLAY_1 DM_PLY1
#define QK_DYNAMIC_MACRO_PLAY_2 0x7102
#define QK_DYNAMIC_MACRO_RECORD_STOP DM_RSTP
'''
core=(qmk_root/'quantum/process_keycode/process_dynamic_macro.c').read_text()
core=re.sub(r'^#include.*$', '', core, flags=re.M)
core=re.sub(r'__attribute__\(\(weak\)\) bool dynamic_macro_\w+_user\([^)]*\) \{.*?^\}', '', core, flags=re.S|re.M)
(here/'dynamic_macro_core.c').write_text(core)

(here/'mock.h').write_text(header)
(here/'keychron_common.h').write_text('#pragma once\n')
(here/'dynamic_keymap.h').write_text('#pragma once\n')
(here/'quantum.h').write_text('#include "mock.h"\n')
test='''
#include <stdio.h>
int main(void){
 keyrecord_t press={.event={.pressed=true}},release={.event={.pressed=false}};
 stored_extra[2][10]=DM_PLY1;stored_extra[2][9]=stored_extra[3][6]=stored_extra[5][16]=KC_TRNS;stored_extra[3][7]=SHELL_HISTORY;
 stored_square=LNX_OVERVIEW;
 keyboard_post_init_user(); assert(keymap_config.autocorrect_enable&&stored_square==LNX_PASTE&&stored_fn_l==LIST_LONG);
 assert(stored_extra[2][10]==PROCESS_LIST&&stored_extra[2][9]==DM_PLY1&&stored_extra[3][6]==SHELL_HISTORY&&stored_extra[3][7]==KC_TRNS&&stored_extra[5][16]==LNX_CALC);
 stored_extra[2][10]=stored_extra[3][6]=stored_extra[3][7]=KC_F15;keyboard_post_init_user();assert(stored_extra[2][10]==KC_F15&&stored_extra[3][6]==KC_F15&&stored_extra[3][7]==KC_F15);
 stored_square=KC_F15;keyboard_post_init_user();assert(stored_square==KC_F15);
 uint16_t k=KC_A; uint8_t buf=9,m=0;
 assert(!process_autocorrect_user(&k,&press,&buf,&m)&&buf==0);
 assert(process_record_user(WIN_SIG,&press)); assert(!literal[0]);
 assert(process_record_user(KC_BSPC,&press));
 // Enter Linux from Mac with Fn held; the default layer survives macro layer_clear.
 layer_state=1UL<<MAC_FN; process_record_user(LINUX_MODE,&press);
 assert(linux_mode()&&default_layer_state==(1UL<<LINUX_BASE)&&layer_state==0);
 assert(rgb_mode==RGB_MATRIX_TYPING_HEATMAP);
 assert(process_autocorrect_user(&k,&press,&buf,&m)&&default_handler_calls==1);
 process_record_user(AC_SWITCH,&press); buf=9;
 assert(!linux_autocorrect&&!process_autocorrect_user(&k,&press,&buf,&m)&&buf==0);
 rgb_matrix_indicators_advanced_user(0,1);assert(led_red==255&&led_green==100);
 process_record_user(AC_SWITCH,&press);
 rgb_matrix_indicators_advanced_user(0,1);assert(led_red==0&&led_green==180);
 held_mods=1;weak_mods=2;oneshot=2;
 process_record_user(WIN_SIG,&press);
 assert(!strcmp(literal,"Thanks,\\nAlastair.\\n"));
 assert(held_mods==1&&weak_mods==2&&oneshot==2);
 literal[0]=0;process_record_user(WIN_SIG,&release);assert(!literal[0]);
 process_record_user(UPDIR,&press);assert(!strcmp(literal,"../"));
 assert(autocorrect_resets>=5);
 dynamic_macro_record_start_user(1);layer_clear();assert(linux_mode());
 rgb_matrix_indicators_advanced_user(0,1);assert(led_red==255&&led_green==0);
 assert(!dynamic_macro_valid_key_user(LINUX_MODE,&press));
 assert(dynamic_macro_valid_key_user(KC_A,&press));
 dynamic_macro_record_end_user(1);process_record_user(LINUX_MODE,&press);
 assert(!macro_recording&&!linux_mode()&&default_layer_state==1&&rgb_mode==7);
 // Enter from Windows, return there, and gate autocorrect again.
 default_layer_set(1UL<<WIN_BASE);process_record_user(LINUX_MODE,&press);
 assert(linux_mode());process_record_user(LNX_COPY,&press);assert(last_tap==LCTL(LSFT(KC_C)));
 process_record_user(LNX_PASTE,&press);assert(last_tap==LCTL(LSFT(KC_V)));
 literal[0]=0;process_record_user(LIST_LONG,&press);assert(!strcmp(literal,"ls -ltr\\n"));
 literal[0]=0;process_record_user(LIST_LONG,&release);assert(!literal[0]);
 process_record_user(KC_LALT,&press);literal[0]=0;
 process_record_user(KC_L,&press);assert(!strcmp(literal,"ls -ltr\\n")&&!butterfly_forwarded);
 literal[0]=0;process_record_user(KC_L,&release);assert(!literal[0]);
 int listing_taps=taps;process_record_user(KC_LALT,&release);assert(taps==listing_taps);
 // Commands work through either trigger, only on press, without leaking Alt.
 uint16_t actions[]={PROCESS_LIST,SHELL_HISTORY,LNX_CALC};
 uint16_t partners[]={KC_P,KC_H,KC_P0};
 const char *commands[]={"ps auxw|more\\n","history\\n"};
 for(int i=0;i<3;i++){
  literal[0]=0;int before=taps;
  assert(!process_record_user(actions[i],&press));
  if(i<2)assert(!strcmp(literal,commands[i]));else assert(last_tap==KC_CALC&&taps==before+1);
  literal[0]=0;before=taps;assert(!process_record_user(actions[i],&release));assert(!literal[0]&&taps==before);
  process_record_user(KC_LALT,&press);literal[0]=0;before=taps;
  assert(!process_record_user(partners[i],&press));assert(!butterfly_forwarded&&!get_mods());
  if(i<2)assert(!strcmp(literal,commands[i]));else assert(last_tap==KC_CALC&&taps==before+1);
  literal[0]=0;before=taps;process_record_user(partners[i],&release);process_record_user(KC_LALT,&release);
  assert(!literal[0]&&taps==before);
 }
 // Left butterfly: clipboard chords consume Alt, ordinary shortcuts forward it.
 held_mods=weak_mods=oneshot=0;
 process_record_user(KC_LALT,&press);assert(butterfly_held&&!get_mods());
 process_record_user(LNX_COPY,&press);assert(last_tap==LCTL(KC_C));
 int clip_taps=taps;
 process_record_user(LNX_COPY,&release);process_record_user(KC_LALT,&release);
 assert(taps==clip_taps&&!butterfly_held); // no leaked Alt tap/menu
 process_record_user(KC_LALT,&press);process_record_user(LNX_PASTE,&press);
 assert(last_tap==LCTL(KC_V));process_record_user(KC_LALT,&release);
 process_record_user(KC_LALT,&press);process_record_user(KC_TAB,&press);
 assert(butterfly_forwarded&&last_tap==KC_LALT&&(held_mods&(1U<<(KC_LALT-224))));
 process_record_user(KC_LALT,&release);assert(!butterfly_forwarded&&!(held_mods&(1U<<(KC_LALT-224))));
 process_record_user(KC_LALT,&press);process_record_user(KC_LALT,&release);
 assert(last_tap==KC_LALT); // standalone key retains existing behaviour
 held_mods=1;weak_mods=2;oneshot=2;
 process_record_user(LNX_COPY,&press);assert(last_tap==LCTL(LSFT(KC_C)));
 assert(held_mods==1&&weak_mods==2&&oneshot==2);
 held_mods=weak_mods=oneshot=0;
 process_record_user(LNX_TERM,&press);assert(last_tap==LCTL(LALT(KC_T)));
 process_record_user(LINUX_MODE,&press);assert(default_layer_state==(1UL<<WIN_BASE));
 buf=9;assert(!process_autocorrect_user(&k,&press,&buf,&m)&&buf==0);
 // The real keyboard callback selects a stock default before invoking our hook.
 process_record_user(LINUX_MODE,&press);
 default_layer_set(1UL<<MAC_BASE);
 assert(!linux_mode()&&!macro_recording&&rgb_mode==7&&standard_layer==MAC_BASE);
 assert((shift_delete.layers&(1UL<<LINUX_BASE))&&!(shift_delete.layers&(1UL<<WIN_BASE)));
 // A forced unchanged rear-switch report on wake must preserve Linux mode.
 process_record_user(LINUX_MODE,&press);
 process_record_user(AC_SWITCH,&press);bool saved_autocorrect=linux_autocorrect;
 layer_state=1UL<<LINUX_FN;
 default_layer_set(1UL<<standard_layer);
 assert(linux_mode()&&custom_rgb_active&&linux_autocorrect==saved_autocorrect);
 assert(layer_state==(1UL<<LINUX_FN));
 process_record_user(LINUX_MODE,&press);assert(!linux_mode());
 // Exercise QMK's real dynamic-macro engine, including its layer_clear calls.
 process_record_user(LINUX_MODE,&press);
 release.event.time=DM_REC1;process_dynamic_macro(DM_REC1,&release);
 assert(macro_recording&&linux_mode()&&macro_id==1);
 keyrecord_t letter={.event={.pressed=true,.time=KC_A}};
 process_record(&letter);letter.event.pressed=false;process_record(&letter);
 process_dynamic_macro(DM_RSTP,&press);assert(!macro_recording&&macro_id==0);
 int before=replayed_letters;
 layer_state=1UL<<LINUX_FN;
 process_dynamic_macro(DM_PLY1,&release);
 assert(replayed_letters==before+1&&linux_mode()&&layer_state==(1UL<<LINUX_FN));
 puts("PASS: mode isolation, both stock return paths, rear switch recovery, autocorrect gate/indicator, literal macros/modifier restoration, macro recording/replay with QMK core, clipboard modes/modifier isolation, desktop shortcuts, override scope");
}
'''
dispatcher='''
static int replayed_letters;
void process_record(keyrecord_t *record){
 uint16_t code=record->event.time;
 if(!process_dynamic_macro(code,record))return;
 if(!process_record_user(code,record))return;
 if(record->event.pressed&&code==KC_A)replayed_letters++;
}
'''
(here/'test.c').write_text('#include "mock.h"\n#include "'+str(keymap)+'"\n#include "dynamic_macro_core.c"\n'+dispatcher+test)
subprocess.run(['cc','-std=c11','-I'+str(here),'-DQMK_KEYBOARD_H="mock.h"',str(here/'test.c'),'-o',str(here/'test')],check=True)
subprocess.run([str(here/'test')],check=True)
