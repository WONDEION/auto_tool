#ifndef BUILD_LK
#include <linux/string.h>
#endif
#include "lcm_drv.h"

// ---------------------------------------------------------------------------
//  Local Constants
// ---------------------------------------------------------------------------

#define FRAME_WIDTH  (480)
#define FRAME_HEIGHT (960)

#ifndef TRUE
    #define   TRUE     1
#endif
 
#ifndef FALSE
    #define   FALSE    0
#endif

#define REGFLAG_DELAY                                       0XFFE
#define REGFLAG_END_OF_TABLE                                0xFFF   // END OF REGISTERS MARKER

#define LCM_ID_gc9503v	0x9504

// ---------------------------------------------------------------------------
//  Local Variables
// ---------------------------------------------------------------------------

static struct LCM_UTIL_FUNCS lcm_util = {0};

#define SET_RESET_PIN(v)    (lcm_util.set_reset_pin((v)))

//extern int IMM_GetOneChannelValue(int dwChannel, int data[4], int *rawdata);



#define UDELAY(n) 											(lcm_util.udelay(n))
#define MDELAY(n) 											(lcm_util.mdelay(n))


// ---------------------------------------------------------------------------
//  Local Functions
// ---------------------------------------------------------------------------

#define dsi_set_cmdq_V2(cmd, count, ppara, force_update)            lcm_util.dsi_set_cmdq_V2(cmd, count, ppara, force_update)
#define dsi_set_cmdq(pdata, queue_size, force_update)       lcm_util.dsi_set_cmdq(pdata, queue_size, force_update)
#define wrtie_cmd(cmd)                                      lcm_util.dsi_write_cmd(cmd)
#define write_regs(addr, pdata, byte_nums)                  lcm_util.dsi_write_regs(addr, pdata, byte_nums)
#define read_reg(cmd)											lcm_util.dsi_dcs_read_lcm_reg(cmd)
#define read_reg_v2(cmd, buffer, buffer_size)                   lcm_util.dsi_dcs_read_lcm_reg_v2(cmd, buffer, buffer_size)


#define   LCM_DSI_CMD_MODE							0

struct LCM_setting_table {
	unsigned cmd;
	unsigned char count;
	unsigned char para_list[64];
};

static struct LCM_setting_table lcm_initialization_setting[] = 
{

{0xF0,5,{0x55,0xAA,0x52,0x08,0x00}},
{0xF6,2,{0x5A,0x87}},
{0xC1,1,{0x3F}},
{0xC2,1,{0x0E}},
{0xC6,1,{0xF8}},
{0xCD,1,{0x25}},
{0xC9,1,{0x10}},
{0xF8,1,{0x8A}},
{0xAC,1,{0x65}},
{0xA7,1,{0x47}},
{0xA0,1,{0xFF}},
{0x86,4,{0x99,0xA4,0xA4,0x61}},
{0x87,3,{0x04,0x03,0x66}},
{0xFA,4,{0x00,0x00,0x00,0x04}},
{0xA3,1,{0x6E}},
{0xFD,3,{0x28,0x3C,0x00}},
{0x9A,1,{0x4E}},
{0x9B,1,{0x3C}},
{0x82,2,{0x0E,0x0E}},
{0xB1,1,{0x10}},
{0x7A,2,{0x0F,0x13}},
{0x7B,2,{0x0F,0x13}},
{0x6D,32,{0x1E,0x1E,0x1E,0x03,0x01,0x09,0x0F,0x0B,0x0D,0x05,0x07,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x1E,0x08,0x06,0x0E,0x0C,0x10,0x0A,0x02,0x04,0x1E,0x1E,0x1E}},
{0x64,16,{0x28,0x05,0x03,0xC2,0x03,0x03,0x28,0x04,0x03,0xC3,0x03,0x03,0x01,0x60,0x01,0x60}},
{0x65,16,{0x28,0x01,0x03,0xC6,0x03,0x03,0x28,0x00,0x03,0xC7,0x03,0x03,0x01,0x60,0x01,0x60}},
{0x66,16,{0x20,0x01,0x03,0xC8,0x03,0x03,0x20,0x02,0x03,0xC9,0x03,0x03,0x01,0x60,0x01,0x60}},
{0x67,16,{0x28,0x03,0x03,0xC4,0x03,0x03,0x28,0x02,0x03,0xC5,0x03,0x03,0x01,0x60,0x01,0x60}},
{0x60,8,{0x38,0x09,0x60,0x60,0x38,0x08,0x60,0x60}},
{0x61,8,{0x38,0x07,0x60,0x60,0x38,0x06,0x60,0x60}},
{0x62,8,{0x33,0xBB,0x60,0x60,0x33,0xBC,0x60,0x60}},
{0x63,8,{0x33,0xBD,0x60,0x60,0x33,0xBE,0x60,0x60}},
{0x69,7,{0x11,0x24,0x11,0x24,0x44,0x22,0x08}},
{0x6B,1,{0x07}},
/*
{0xD1,52,{0x00,0x00,0x00,0x10,0x00,0x34,0x00,0x50,0x00,0x69,0x00,0x90,0x00,0xB0,0x00,0xE1,0x01,0x07,0x01,0x4B,0x01,0x80,0x01,0xCF,0x02,0x0F,0x02,0x12,0x02,0x50,0x02,0x9A,0x02,0xCF,0x03,0x10,0x03,0x3B,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
{0xD2,52,{0x00,0x00,0x00,0x10,0x00,0x34,0x00,0x50,0x00,0x69,0x00,0x90,0x00,0xB0,0x00,0xE1,0x01,0x07,0x01,0x4B,0x01,0x80,0x01,0xCF,0x02,0x0F,0x02,0x12,0x02,0x50,0x02,0x9A,0x02,0xCF,0x03,0x10,0x03,0x3B,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
{0xD3,52,{0x00,0x00,0x00,0x10,0x00,0x34,0x00,0x50,0x00,0x69,0x00,0x90,0x00,0xB0,0x00,0xE1,0x01,0x07,0x01,0x4B,0x01,0x80,0x01,0xCF,0x02,0x0F,0x02,0x12,0x02,0x50,0x02,0x9A,0x02,0xCF,0x03,0x10,0x03,0x3B,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
{0xD4,52,{0x00,0x00,0x00,0x10,0x00,0x34,0x00,0x50,0x00,0x69,0x00,0x90,0x00,0xB0,0x00,0xE1,0x01,0x07,0x01,0x4B,0x01,0x80,0x01,0xCF,0x02,0x0F,0x02,0x12,0x02,0x50,0x02,0x9A,0x02,0xCF,0x03,0x10,0x03,0x3B,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
{0xD5,52,{0x00,0x00,0x00,0x10,0x00,0x34,0x00,0x50,0x00,0x69,0x00,0x90,0x00,0xB0,0x00,0xE1,0x01,0x07,0x01,0x4B,0x01,0x80,0x01,0xCF,0x02,0x0F,0x02,0x12,0x02,0x50,0x02,0x9A,0x02,0xCF,0x03,0x10,0x03,0x3B,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
{0xD6,52,{0x00,0x00,0x00,0x10,0x00,0x34,0x00,0x50,0x00,0x69,0x00,0x90,0x00,0xB0,0x00,0xE1,0x01,0x07,0x01,0x4B,0x01,0x80,0x01,0xCF,0x02,0x0F,0x02,0x12,0x02,0x50,0x02,0x9A,0x02,0xCF,0x03,0x10,0x03,0x3B,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
*/
	{0xD1,52,{0x00,0x00,0x00,0x10,0x00,0x37,0x00,0x55,0x00,0x6E,0x00,0x97,0x00,0xB8,0x00,0xEB,0x01,0x18,0x01,0x5D,0x01,0x92,0x01,0xE1,0x02,0x1F,0x02,0x22,0x02,0x5D,0x02,0xA4,0x02,0xD2,0x03,0x13,0x03,0x3D,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
	{0xD2,52,{0x00,0x00,0x00,0x10,0x00,0x37,0x00,0x55,0x00,0x6E,0x00,0x97,0x00,0xB8,0x00,0xEB,0x01,0x18,0x01,0x5D,0x01,0x92,0x01,0xE1,0x02,0x1F,0x02,0x22,0x02,0x5D,0x02,0xA4,0x02,0xD2,0x03,0x13,0x03,0x3D,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
	{0xD3,52,{0x00,0x00,0x00,0x10,0x00,0x37,0x00,0x55,0x00,0x6E,0x00,0x97,0x00,0xB8,0x00,0xEB,0x01,0x18,0x01,0x5D,0x01,0x92,0x01,0xE1,0x02,0x1F,0x02,0x22,0x02,0x5D,0x02,0xA4,0x02,0xD2,0x03,0x13,0x03,0x3D,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
	{0xD4,52,{0x00,0x00,0x00,0x10,0x00,0x37,0x00,0x55,0x00,0x6E,0x00,0x97,0x00,0xB8,0x00,0xEB,0x01,0x18,0x01,0x5D,0x01,0x92,0x01,0xE1,0x02,0x1F,0x02,0x22,0x02,0x5D,0x02,0xA4,0x02,0xD2,0x03,0x13,0x03,0x3D,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
	{0xD5,52,{0x00,0x00,0x00,0x10,0x00,0x37,0x00,0x55,0x00,0x6E,0x00,0x97,0x00,0xB8,0x00,0xEB,0x01,0x18,0x01,0x5D,0x01,0x92,0x01,0xE1,0x02,0x1F,0x02,0x22,0x02,0x5D,0x02,0xA4,0x02,0xD2,0x03,0x13,0x03,0x3D,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},
	{0xD6,52,{0x00,0x00,0x00,0x10,0x00,0x37,0x00,0x55,0x00,0x6E,0x00,0x97,0x00,0xB8,0x00,0xEB,0x01,0x18,0x01,0x5D,0x01,0x92,0x01,0xE1,0x02,0x1F,0x02,0x22,0x02,0x5D,0x02,0xA4,0x02,0xD2,0x03,0x13,0x03,0x3D,0x03,0x6E,0x03,0x8F,0x03,0xB3,0x03,0xC9,0x03,0xE4,0x03,0xF9,0x03,0xFF}},


 {0x11, 0,{0x00}},
{REGFLAG_DELAY, 120, {}},
{0x29, 0,{0x00}},
{REGFLAG_DELAY, 40, {}},
{REGFLAG_END_OF_TABLE, 0x00, {}}	
	

};

//p1
//0xc5
//8172

//p1 be

static struct LCM_setting_table lcm_sleep_in_setting[] =
{
 // 防液晶极化
        {0x6C, 1,{0x60}},
	{REGFLAG_DELAY, 20, {}},
	{0xB1, 1,{0x00}},
	{0xFA, 4,{0x7F, 0x00, 0x00, 0x00}},
	{REGFLAG_DELAY, 20, {}},
	{0x6c,1,{0x50}}, 
	{REGFLAG_DELAY, 10, {}},

	{0x28, 0,{0x00}},	
	{REGFLAG_DELAY, 50, {}},  
	{0x10, 0,{0x00}},
	{REGFLAG_DELAY, 20, {}},
	
         //下电代码
	{0xF0,5,{0x55,0xaa,0x52,0x08,0x00}},
	{0xc2,1,{0xce}},
	{0xc3,1,{0xcd}},
	{0xc6,1,{0xfc}},
	{0xc5,1,{0x03}},
	{0xcd,1,{0x64}},
	{0xc4,1,{0xff}},///REG85 EN
	
	{0xc9,1,{0xcd}},
	{0xF6,2,{0x5a,0x87}},
	{0xFd,3,{0xaa,0xaa, 0x0a}},
	{0xFe,2,{0x6a,0x0a}},
	{0x78,2,{0x2a,0xaa}},
	{0x92,2,{0x17,0x08}},
	{0x77,2,{0xaa,0x2a}},
	{0x76,2,{0xaa,0xaa}},

    {0x84,1,{0x00}},
	{0x78,2,{0x2b,0xba}},
	{0x89,1,{0x73}},
	{0x88,1,{0x3A}},
	{0x85,1,{0xB0}},
	{0x76,2,{0xeb,0xaa}},
	{0x94,1,{0x80}},
	{0x87,3,{0x04,0x07,0x30}},					
	{0x93,1,{0x27}},
	{0xaf,1,{0x02}},
	

       {REGFLAG_END_OF_TABLE, 0x00, {}}
};


static void push_table(struct LCM_setting_table *table, unsigned int count, unsigned char force_update)
{
	unsigned int i;

    for(i = 0; i < count; i++)
    {
		
        unsigned cmd;
        cmd = table[i].cmd;
		
        switch (cmd)
        {
			
            case REGFLAG_DELAY :
                MDELAY(table[i].count);
                break;
				
            case REGFLAG_END_OF_TABLE :
                break;
				
            default:
				dsi_set_cmdq_V2(cmd, table[i].count, table[i].para_list, force_update);
       	}
    }
	
}

static void init_lcm_registers(void)
{
	push_table(lcm_initialization_setting, sizeof(lcm_initialization_setting) / sizeof(struct LCM_setting_table), 1);
}


// ---------------------------------------------------------------------------
//  LCM Driver Implementations
// ---------------------------------------------------------------------------

static void lcm_set_util_funcs(const struct LCM_UTIL_FUNCS *util)
{
    memcpy(&lcm_util, util, sizeof(struct LCM_UTIL_FUNCS));
}


static void lcm_get_params(struct LCM_PARAMS *params)
{

		memset(params, 0, sizeof(struct LCM_PARAMS));
	
		params->type   = LCM_TYPE_DSI;

		params->width  = FRAME_WIDTH;
		params->height = FRAME_HEIGHT;

		// enable tearing-free
		params->dbi.te_mode 				= LCM_DBI_TE_MODE_VSYNC_ONLY;
		params->dbi.te_edge_polarity		= LCM_POLARITY_RISING;

#if (LCM_DSI_CMD_MODE)
		params->dsi.mode   = CMD_MODE;
#else
		params->dsi.mode   = SYNC_PULSE_VDO_MODE;
#endif
	
		// DSI
		/* Command mode setting */
		params->dsi.LANE_NUM				= LCM_TWO_LANE;
		//The following defined the fomat for data coming from LCD engine.
		params->dsi.data_format.color_order = LCM_COLOR_ORDER_RGB;
		params->dsi.data_format.trans_seq   = LCM_DSI_TRANS_SEQ_MSB_FIRST;
		params->dsi.data_format.padding     = LCM_DSI_PADDING_ON_LSB;
		params->dsi.data_format.format      = LCM_DSI_FORMAT_RGB888;

		// Highly depends on LCD driver capability.
		// Not support in MT6573
		params->dsi.packet_size=256;
                params->dsi.word_count=480*3;   
		// Video mode setting		
		params->dsi.intermediat_buffer_num = 0;

		params->dsi.PS=LCM_PACKED_PS_24BIT_RGB888;

		params->dsi.vertical_sync_active				= 2; //4 -> 2
		params->dsi.vertical_backporch					= 20; //22 -> 15
		params->dsi.vertical_frontporch					= 22;  //22 -> 8
		params->dsi.vertical_active_line				= FRAME_HEIGHT;

		params->dsi.horizontal_sync_active				= 10;  //8
		params->dsi.horizontal_backporch				= 30;//40;  //30
		params->dsi.horizontal_frontporch				= 30;//40;  //30
		params->dsi.horizontal_active_pixel				= FRAME_WIDTH;

		//1 Every lane speed
	//	params->dsi.pll_div1=0;		// div1=0,1,2,3;div1_real=1,2,4,4 ----0: 546Mbps  1:273Mbps
	//	params->dsi.pll_div2=1;		// div2=0,1,2,3;div1_real=1,2,4,4	
		//params->dsi.fbk_div =16; // 19;    // fref=26MHz, fvco=fref*(fbk_div+1)*2/(div1_real*div2_real)	
		params->dsi.PLL_CLOCK = 200; //208 195 212 
    params->dsi.ssc_disable = 1;  // ssc disable control (1: disable, 0: enable, default: 0)
		#if 1
		params->dsi.clk_lp_per_line_enable = 0;
       /* params->dsi.noncont_clock				= TRUE; 
		params->dsi.noncont_clock_period			= 1;*/
		
	    params->dsi.cont_clock  = 1; //ADD++
		
		
	params->dsi.esd_check_enable = 1;
	params->dsi.customization_esd_check_enable = 1;
	params->dsi.lcm_esd_check_table[0].cmd          = 0x0a;
	params->dsi.lcm_esd_check_table[0].count        = 1;
	params->dsi.lcm_esd_check_table[0].para_list[0] = 0x9c;

		#endif
		
#if 0
		/* ESD or noise interference recovery For video mode LCM only. */ // Send TE packet to LCM in a period of n frames and check the response. 
		//params->dsi.lcm_int_te_monitor = FALSE; 
		//params->dsi.lcm_int_te_period = 1; // Unit : frames 
 
		// Need longer FP for more opportunity to do int. TE monitor applicably. 
		if(params->dsi.lcm_int_te_monitor) 
			params->dsi.vertical_frontporch *= 2; 
			params->dsi.lcm_int_te_period = 1; // Unit : frames 
		// Monitor external TE (or named VSYNC) from LCM once per 2 sec. (LCM VSYNC must be wired to baseband TE pin.) 
		//params->dsi.lcm_ext_te_monitor = FALSE; 
		params->dsi.lcm_ext_te_monitor = 0; // Non-continuous clock 
		params->dsi.noncont_clock = 1; 
		params->dsi.noncont_clock_period = 2; // Unit : frames
#endif

	
	
}

static void lcm_init(void)
{

    SET_RESET_PIN(1);
    MDELAY(10);
    SET_RESET_PIN(0);
    MDELAY(20);//Must > 10ms
    SET_RESET_PIN(1);
    MDELAY(160);

	init_lcm_registers();

}

static void lcm_suspend(void)
{

	push_table(lcm_sleep_in_setting, sizeof(lcm_sleep_in_setting) / sizeof(struct LCM_setting_table), 1);


/*
    SET_RESET_PIN(1);
    MDELAY(10);
    SET_RESET_PIN(0);
    MDELAY(20);//Must > 10ms
    SET_RESET_PIN(1);
    MDELAY(120);*/
}


static void lcm_resume(void)
{

	lcm_init();

}

#if (LCM_DSI_CMD_MODE)
static void lcm_update(unsigned int x, unsigned int y,
                       unsigned int width, unsigned int height)
{
	unsigned int x0 = x;
	unsigned int y0 = y;
	unsigned int x1 = x0 + width - 1;
	unsigned int y1 = y0 + height - 1;

	unsigned char x0_MSB = ((x0>>8)&0xFF);
	unsigned char x0_LSB = (x0&0xFF);
	unsigned char x1_MSB = ((x1>>8)&0xFF);
	unsigned char x1_LSB = (x1&0xFF);
	unsigned char y0_MSB = ((y0>>8)&0xFF);
	unsigned char y0_LSB = (y0&0xFF);
	unsigned char y1_MSB = ((y1>>8)&0xFF);
	unsigned char y1_LSB = (y1&0xFF);

	unsigned int data_array[16];

	data_array[0]= 0x00053902;
	data_array[1]= (x1_MSB<<24)|(x0_LSB<<16)|(x0_MSB<<8)|0x2a;
	data_array[2]= (x1_LSB);
	dsi_set_cmdq(&data_array, 3, 1);

	data_array[0]= 0x00053902;
	data_array[1]= (y1_MSB<<24)|(y0_LSB<<16)|(y0_MSB<<8)|0x2b;
	data_array[2]= (y1_LSB);
	dsi_set_cmdq(&data_array, 3, 1);

	data_array[0]= 0x00290508; //HW bug, so need send one HS packet
	dsi_set_cmdq(&data_array, 1, 1);

	data_array[0]= 0x002c3909;
	dsi_set_cmdq(&data_array, 1, 0);

}
#endif

static unsigned int lcm_compare_id(void)
{
    	int id=0;
	unsigned char buffer[4];
	unsigned int array[16];  
	char id_high=0;
	char id_low=0;
        
	SET_RESET_PIN(1);
	MDELAY(10);
	SET_RESET_PIN(0);
	MDELAY(10);
	SET_RESET_PIN(1);
	MDELAY(120);


	array[0] = 0x00033700; //
	dsi_set_cmdq(array, 1, 1);
	read_reg_v2(0x04, &buffer[0], 3);

    id_high=buffer[1];
    id_low=buffer[2];
    id=(id_high<<8)| id_low;
#ifdef BUILD_LK
	printf("gc9503 _wvga_dsi_vdo_lcm_drv %s:0x%2x,0x%2x,0x%2x,0x%2x id=0x%x\n", __func__,buffer[0],buffer[1],buffer[2],buffer[3], id);
#else
	printk("gc9503 _wvga_dsi_vdo_lcm_drv %s:0x%2x,0x%2x,0x%2x,0x%2x id=0x%x\n", __func__,buffer[0],buffer[1],buffer[2],buffer[3], id);
#endif 
    return ((0x9504 == id) ? 1:0);

}

struct LCM_DRIVER gc9503v_fwvgaplus_dsi_vdo_zhongguangdian_lcm_drv = 
{
    .name			= "gc9503v_fwvgaplus_dsi_vdo_zhongguangdian_lcm_drv",
	.set_util_funcs = lcm_set_util_funcs,
	.get_params     = lcm_get_params,
	.init           = lcm_init,
	.suspend        = lcm_suspend,
	.resume         = lcm_resume,
	.compare_id    = lcm_compare_id,	
#if (LCM_DSI_CMD_MODE)
    .update         = lcm_update,
#endif
};
