// 临池录常量库（移植自小程序 utils/constants.js）
window.SHUFA_DATA = {
 "PAPER_TYPES": {
  "sizhi_sikai": {
   "id": "sizhi_sikai",
   "name": "四尺四开",
   "keywords": [
    "四尺四开"
   ],
   "type": "sheet",
   "category": "四尺系列",
   "dimensions": {
    "width": 34,
    "height": 69,
    "unit": "cm"
   },
   "lengthPerSheet": 0.69,
   "isDefault": false
  },
  "sizhi_duikai": {
   "id": "sizhi_duikai",
   "name": "四尺对开",
   "keywords": [
    "四尺对开"
   ],
   "type": "sheet",
   "category": "四尺系列",
   "dimensions": {
    "width": 34,
    "height": 138,
    "unit": "cm"
   },
   "lengthPerSheet": 1.38,
   "isDefault": true
  },
  "sizhi_zhengzhang": {
   "id": "sizhi_zhengzhang",
   "name": "四尺整张",
   "keywords": [
    "四尺整张",
    "四尺全张"
   ],
   "type": "sheet",
   "category": "四尺系列",
   "dimensions": {
    "width": 69,
    "height": 138,
    "unit": "cm"
   },
   "lengthPerSheet": 1.38,
   "isDefault": false
  },
  "sizhi_sankai": {
   "id": "sizhi_sankai",
   "name": "四尺三开",
   "keywords": [
    "四尺三开"
   ],
   "type": "sheet",
   "category": "四尺系列",
   "dimensions": {
    "width": 46,
    "height": 69,
    "unit": "cm"
   },
   "lengthPerSheet": 0.69,
   "isDefault": false
  },
  "liuchi_duikai": {
   "id": "liuchi_duikai",
   "name": "六尺对开",
   "keywords": [
    "六尺对开"
   ],
   "type": "sheet",
   "category": "六尺系列",
   "dimensions": {
    "width": 46,
    "height": 180,
    "unit": "cm"
   },
   "lengthPerSheet": 1.8,
   "isDefault": false
  },
  "liuchi_zhengzhang": {
   "id": "liuchi_zhengzhang",
   "name": "六尺整张",
   "keywords": [
    "六尺整张"
   ],
   "type": "sheet",
   "category": "六尺系列",
   "dimensions": {
    "width": 97,
    "height": 180,
    "unit": "cm"
   },
   "lengthPerSheet": 1.8,
   "isDefault": false
  },
  "yichi_doufang": {
   "id": "yichi_doufang",
   "name": "一尺斗方",
   "keywords": [
    "一尺斗方"
   ],
   "type": "sheet",
   "category": "斗方系列",
   "dimensions": {
    "width": 33,
    "height": 33,
    "unit": "cm"
   },
   "lengthPerSheet": 0.33,
   "isDefault": false
  },
  "erchi_doufang": {
   "id": "erchi_doufang",
   "name": "二尺斗方",
   "keywords": [
    "二尺斗方"
   ],
   "type": "sheet",
   "category": "斗方系列",
   "dimensions": {
    "width": 46,
    "height": 46,
    "unit": "cm"
   },
   "lengthPerSheet": 0.46,
   "isDefault": false
  },
  "xiaokaijian": {
   "id": "xiaokaijian",
   "name": "小楷笺",
   "keywords": [
    "小楷笺",
    "小楷纸"
   ],
   "type": "sheet",
   "category": "小楷专用",
   "dimensions": {
    "width": 17,
    "height": 28,
    "unit": "cm"
   },
   "lengthPerSheet": 0.28,
   "isDefault": false
  },
  "scroll_20m": {
   "id": "scroll_20m",
   "name": "20米长卷",
   "keywords": [
    "20米长卷",
    "二十米长卷"
   ],
   "type": "scroll",
   "category": "长卷系列",
   "dimensions": {
    "width": 35,
    "maxLength": 2000,
    "unit": "cm"
   },
   "lengthPerSheet": 20,
   "isDefault": false
  },
  "scroll_30m": {
   "id": "scroll_30m",
   "name": "30米长卷",
   "keywords": [
    "30米长卷",
    "三十米长卷"
   ],
   "type": "scroll",
   "category": "长卷系列",
   "dimensions": {
    "width": 35,
    "maxLength": 3000,
    "unit": "cm"
   },
   "lengthPerSheet": 30,
   "isDefault": false
  },
  "scroll_50m": {
   "id": "scroll_50m",
   "name": "50米长卷",
   "keywords": [
    "50米长卷",
    "五十米长卷"
   ],
   "type": "scroll",
   "category": "长卷系列",
   "dimensions": {
    "width": 35,
    "maxLength": 5000,
    "unit": "cm"
   },
   "lengthPerSheet": 50,
   "isDefault": false
  },
  "scroll_100m": {
   "id": "scroll_100m",
   "name": "100米长卷",
   "keywords": [
    "100米长卷",
    "一百米长卷"
   ],
   "type": "scroll",
   "category": "长卷系列",
   "dimensions": {
    "width": 35,
    "maxLength": 10000,
    "unit": "cm"
   },
   "lengthPerSheet": 100,
   "isDefault": false
  },
  "scroll_default": {
   "id": "scroll_default",
   "name": "长卷（未指定）",
   "keywords": [
    "长卷"
   ],
   "type": "scroll",
   "category": "长卷系列",
   "dimensions": {
    "width": 35,
    "maxLength": 5000,
    "unit": "cm"
   },
   "lengthPerSheet": 0,
   "isDefault": false
  }
 },
 "FONT_KEYWORDS": [
  "楷书",
  "行书",
  "隶书",
  "草书",
  "篆书",
  "小楷"
 ],
 "PAPER_KEYWORDS": [
  {
   "keywords": [
    "四尺四开"
   ],
   "id": "sizhi_sikai",
   "type": "sheet"
  },
  {
   "keywords": [
    "四尺对开"
   ],
   "id": "sizhi_duikai",
   "type": "sheet"
  },
  {
   "keywords": [
    "四尺整张",
    "四尺全张"
   ],
   "id": "sizhi_zhengzhang",
   "type": "sheet"
  },
  {
   "keywords": [
    "四尺三开"
   ],
   "id": "sizhi_sankai",
   "type": "sheet"
  },
  {
   "keywords": [
    "六尺对开"
   ],
   "id": "liuchi_duikai",
   "type": "sheet"
  },
  {
   "keywords": [
    "六尺整张"
   ],
   "id": "liuchi_zhengzhang",
   "type": "sheet"
  },
  {
   "keywords": [
    "一尺斗方"
   ],
   "id": "yichi_doufang",
   "type": "sheet"
  },
  {
   "keywords": [
    "二尺斗方"
   ],
   "id": "erchi_doufang",
   "type": "sheet"
  },
  {
   "keywords": [
    "小楷笺",
    "小楷纸"
   ],
   "id": "xiaokaijian",
   "type": "sheet"
  },
  {
   "keywords": [
    "20米长卷",
    "二十米长卷"
   ],
   "id": "scroll_20m",
   "type": "scroll"
  },
  {
   "keywords": [
    "30米长卷",
    "三十米长卷"
   ],
   "id": "scroll_30m",
   "type": "scroll"
  },
  {
   "keywords": [
    "50米长卷",
    "五十米长卷"
   ],
   "id": "scroll_50m",
   "type": "scroll"
  },
  {
   "keywords": [
    "100米长卷",
    "一百米长卷"
   ],
   "id": "scroll_100m",
   "type": "scroll"
  },
  {
   "keywords": [
    "长卷"
   ],
   "id": "scroll_default",
   "type": "scroll"
  }
 ],
 "POSTS_LIBRARY": {
  "kaishu": {
   "id": "kaishu",
   "name": "楷书",
   "order": 1,
   "authors": {
    "ouyangxun": {
     "id": "ouyangxun",
     "name": "欧阳询",
     "dynasty": "唐",
     "copybooks": {
      "jiuchenggong": {
       "id": "jiuchenggong",
       "name": "九成宫醴泉铭",
       "versions": {
        "liqiben": {
         "id": "liqiben",
         "name": "李祺本",
         "note": "宋拓本，故宫博物院藏"
        },
        "lihongyiben": {
         "id": "lihongyiben",
         "name": "李鸿裔本",
         "note": "宋拓本"
        }
       }
      },
      "huadusi": {
       "id": "huadusi",
       "name": "化度寺碑",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "宋拓本"
        }
       }
      }
     }
    },
    "yanzhenqing": {
     "id": "yanzhenqing",
     "name": "颜真卿",
     "dynasty": "唐",
     "copybooks": {
      "duobaota": {
       "id": "duobaota",
       "name": "多宝塔碑",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "唐拓本"
        }
       }
      },
      "yanqinli": {
       "id": "yanqinli",
       "name": "颜勤礼碑",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "宋拓本"
        }
       }
      },
      "maguxiantan": {
       "id": "maguxiantan",
       "name": "麻姑仙坛记",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "宋拓本"
        }
       }
      }
     }
    },
    "liugongquan": {
     "id": "liugongquan",
     "name": "柳公权",
     "dynasty": "唐",
     "copybooks": {
      "xuanmita": {
       "id": "xuanmita",
       "name": "玄秘塔碑",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "宋拓本"
        }
       }
      }
     }
    },
    "zhaomengfu": {
     "id": "zhaomengfu",
     "name": "赵孟頫",
     "dynasty": "元",
     "copybooks": {
      "danba": {
       "id": "danba",
       "name": "胆巴碑",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "元拓本"
        }
       }
      }
     }
    },
    "chusuiliang": {
     "id": "chusuiliang",
     "name": "褚遂良",
     "dynasty": "唐",
     "copybooks": {
      "yantash": {
       "id": "yantash",
       "name": "雁塔圣教序",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "宋拓本"
        }
       }
      }
     }
    }
   }
  },
  "xingshu": {
   "id": "xingshu",
   "name": "行书",
   "order": 2,
   "authors": {
    "zhaomengfu_xs": {
     "id": "zhaomengfu_xs",
     "name": "赵孟頫",
     "dynasty": "元",
     "copybooks": {
      "chibifu": {
       "id": "chibifu",
       "name": "前后赤壁赋",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "行书代表作"
        }
       }
      },
      "zhuziganxing": {
       "id": "zhuziganxing",
       "name": "朱子感兴诗",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "行书"
        }
       }
      },
      "xingshuqianziwen": {
       "id": "xingshuqianziwen",
       "name": "行书千字文",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "行书"
        }
       }
      },
      "xianjufu": {
       "id": "xianjufu",
       "name": "闲居赋",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "行书"
        }
       }
      },
      "luoshenfu": {
       "id": "luoshenfu",
       "name": "洛神赋",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "行书"
        }
       }
      },
      "linshengjiaoxu": {
       "id": "linshengjiaoxu",
       "name": "临王羲之圣教序",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "行书"
        }
       }
      },
      "guiqulaici": {
       "id": "guiqulaici",
       "name": "归去来辞",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "行书"
        }
       }
      },
      "qiuxingfu": {
       "id": "qiuxingfu",
       "name": "秋兴赋",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "行书"
        }
       }
      },
      "xiangzhouzhoujintang": {
       "id": "xiangzhouzhoujintang",
       "name": "相州昼锦堂记",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "行书"
        }
       }
      }
     }
    }
   }
  },
  "lishu": {
   "id": "lishu",
   "name": "隶书",
   "order": 3,
   "authors": {
    "unknown_ls": {
     "id": "unknown_ls",
     "name": "佚名",
     "dynasty": "汉",
     "copybooks": {
      "caoquanbei": {
       "id": "caoquanbei",
       "name": "曹全碑",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "汉隶代表作"
        }
       }
      }
     }
    }
   }
  },
  "xiaokai": {
   "id": "xiaokai",
   "name": "小楷",
   "order": 4,
   "authors": {
    "wenzhengming": {
     "id": "wenzhengming",
     "name": "文徵明",
     "dynasty": "明",
     "copybooks": {
      "caotangshizhi": {
       "id": "caotangshizhi",
       "name": "草堂十志",
       "versions": {
        "default": {
         "id": "default",
         "name": "默认版本",
         "note": "小楷代表作"
        }
       }
      }
     }
    }
   }
  }
 },
 "COPYBOOK_LIST": [
  {
   "fontId": "kaishu",
   "fontName": "楷书",
   "authorId": "ouyangxun",
   "authorName": "欧阳询",
   "copybookId": "jiuchenggong",
   "copybookName": "九成宫醴泉铭"
  },
  {
   "fontId": "kaishu",
   "fontName": "楷书",
   "authorId": "ouyangxun",
   "authorName": "欧阳询",
   "copybookId": "huadusi",
   "copybookName": "化度寺碑"
  },
  {
   "fontId": "kaishu",
   "fontName": "楷书",
   "authorId": "yanzhenqing",
   "authorName": "颜真卿",
   "copybookId": "duobaota",
   "copybookName": "多宝塔碑"
  },
  {
   "fontId": "kaishu",
   "fontName": "楷书",
   "authorId": "yanzhenqing",
   "authorName": "颜真卿",
   "copybookId": "yanqinli",
   "copybookName": "颜勤礼碑"
  },
  {
   "fontId": "kaishu",
   "fontName": "楷书",
   "authorId": "yanzhenqing",
   "authorName": "颜真卿",
   "copybookId": "maguxiantan",
   "copybookName": "麻姑仙坛记"
  },
  {
   "fontId": "kaishu",
   "fontName": "楷书",
   "authorId": "liugongquan",
   "authorName": "柳公权",
   "copybookId": "xuanmita",
   "copybookName": "玄秘塔碑"
  },
  {
   "fontId": "kaishu",
   "fontName": "楷书",
   "authorId": "zhaomengfu",
   "authorName": "赵孟頫",
   "copybookId": "danba",
   "copybookName": "胆巴碑"
  },
  {
   "fontId": "kaishu",
   "fontName": "楷书",
   "authorId": "chusuiliang",
   "authorName": "褚遂良",
   "copybookId": "yantash",
   "copybookName": "雁塔圣教序"
  },
  {
   "fontId": "xingshu",
   "fontName": "行书",
   "authorId": "zhaomengfu_xs",
   "authorName": "赵孟頫",
   "copybookId": "chibifu",
   "copybookName": "前后赤壁赋"
  },
  {
   "fontId": "xingshu",
   "fontName": "行书",
   "authorId": "zhaomengfu_xs",
   "authorName": "赵孟頫",
   "copybookId": "zhuziganxing",
   "copybookName": "朱子感兴诗"
  },
  {
   "fontId": "xingshu",
   "fontName": "行书",
   "authorId": "zhaomengfu_xs",
   "authorName": "赵孟頫",
   "copybookId": "xingshuqianziwen",
   "copybookName": "行书千字文"
  },
  {
   "fontId": "xingshu",
   "fontName": "行书",
   "authorId": "zhaomengfu_xs",
   "authorName": "赵孟頫",
   "copybookId": "xianjufu",
   "copybookName": "闲居赋"
  },
  {
   "fontId": "xingshu",
   "fontName": "行书",
   "authorId": "zhaomengfu_xs",
   "authorName": "赵孟頫",
   "copybookId": "luoshenfu",
   "copybookName": "洛神赋"
  },
  {
   "fontId": "xingshu",
   "fontName": "行书",
   "authorId": "zhaomengfu_xs",
   "authorName": "赵孟頫",
   "copybookId": "linshengjiaoxu",
   "copybookName": "临王羲之圣教序"
  },
  {
   "fontId": "xingshu",
   "fontName": "行书",
   "authorId": "zhaomengfu_xs",
   "authorName": "赵孟頫",
   "copybookId": "guiqulaici",
   "copybookName": "归去来辞"
  },
  {
   "fontId": "xingshu",
   "fontName": "行书",
   "authorId": "zhaomengfu_xs",
   "authorName": "赵孟頫",
   "copybookId": "qiuxingfu",
   "copybookName": "秋兴赋"
  },
  {
   "fontId": "xingshu",
   "fontName": "行书",
   "authorId": "zhaomengfu_xs",
   "authorName": "赵孟頫",
   "copybookId": "xiangzhouzhoujintang",
   "copybookName": "相州昼锦堂记"
  },
  {
   "fontId": "lishu",
   "fontName": "隶书",
   "authorId": "unknown_ls",
   "authorName": "佚名",
   "copybookId": "caoquanbei",
   "copybookName": "曹全碑"
  },
  {
   "fontId": "xiaokai",
   "fontName": "小楷",
   "authorId": "wenzhengming",
   "authorName": "文徵明",
   "copybookId": "caotangshizhi",
   "copybookName": "草堂十志"
  }
 ]
};
