/* USER CODE BEGIN Header */

/**

  ******************************************************************************

  * @file           : main.c

  * @brief          : Main program body

  ******************************************************************************

  * @attention

  *

  * Copyright (c) 2026 STMicroelectronics.

  * All rights reserved.

  *

  * This software is licensed under terms that can be found in the LICENSE file

  * in the root directory of this software component.

  * If no LICENSE file comes with this software, it is provided AS-IS.

  *

  ******************************************************************************

  */

/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/

#include "main.h"

#include "string.h"



/* Private includes ----------------------------------------------------------*/

/* USER CODE BEGIN Includes */

#include "math.h"

#include "stdlib.h"

#include <stdio.h>

#include <stdbool.h>



#include "motor_control.h"

#include "sensor_process.h"

#include "ros_comm.h"



/* USER CODE END Includes */



/* Private typedef -----------------------------------------------------------*/

/* USER CODE BEGIN PTD */



/* USER CODE END PTD */



/* Private define ------------------------------------------------------------*/

/* USER CODE BEGIN PD */



//imu

uint8_t rx_data;

uint8_t rx_buffer[11];

uint8_t rx_index = 0;





//odom_enc

static float odom_theta_enc = 0.0f;



/* USER CODE END PD */



/* Private macro -------------------------------------------------------------*/

/* USER CODE BEGIN PM */



/* USER CODE END PM */



/* Private variables ---------------------------------------------------------*/



ETH_TxPacketConfig TxConfig;

ETH_DMADescTypeDef  DMARxDscrTab[ETH_RX_DESC_CNT]; /* Ethernet Rx DMA Descriptors */

ETH_DMADescTypeDef  DMATxDscrTab[ETH_TX_DESC_CNT]; /* Ethernet Tx DMA Descriptors */



ETH_HandleTypeDef heth;



I2C_HandleTypeDef hi2c1;

I2C_HandleTypeDef hi2c2;



TIM_HandleTypeDef htim1;

TIM_HandleTypeDef htim2;

TIM_HandleTypeDef htim3;

TIM_HandleTypeDef htim4;

TIM_HandleTypeDef htim5;

TIM_HandleTypeDef htim9;



UART_HandleTypeDef huart2;

UART_HandleTypeDef huart3;



PCD_HandleTypeDef hpcd_USB_OTG_FS;



/* USER CODE BEGIN PV */

volatile uint8_t emergency_stop = 0;

// 1. UART 수신 관련 변수들

uint8_t received_byte = 0;

uint8_t ros_rx_buffer[50] = {0};  // ROS_CMD_BUFFER_SIZE 크기

uint8_t rx_count = 0;

volatile uint8_t cmd_received = 0;



// 2. 타이밍 및 상태 제어 변수들

uint32_t currentTime = 0;

uint32_t lastCommandReceiveTime = 0;



// 3. 통신 송신용 버퍼

char uart_buf[256] = {0};



#define SPD_PULSES_PER_REV  21.0f



// 오도메트리용 전역 변수 추가

float odom_x = 0.0f;     // x 좌표 (m)

float odom_y = 0.0f;     // y 좌표 (m)



//모터 제어 변수

float control_m1 = 0.0f;

float control_m2 = 0.0f;



float error_rm1 = 0.0f;

float error_rm2 = 0.0f;



float control_rm1 = 0.0f;

float control_rm2 = 0.0f;





/* USER CODE END PV */



/* Private function prototypes -----------------------------------------------*/

void SystemClock_Config(void);

static void MX_GPIO_Init(void);

static void MX_ETH_Init(void);

static void MX_USART3_UART_Init(void);

static void MX_USB_OTG_FS_PCD_Init(void);

static void MX_TIM1_Init(void);

static void MX_TIM3_Init(void);

static void MX_TIM4_Init(void);

static void MX_TIM5_Init(void);

static void MX_TIM2_Init(void);

static void MX_I2C1_Init(void);

static void MX_I2C2_Init(void);

static void MX_USART2_UART_Init(void);

static void MX_TIM9_Init(void);

/* USER CODE BEGIN PFP */



/* USER CODE END PFP */



/* Private user code ---------------------------------------------------------*/

/* USER CODE BEGIN 0 */



uint8_t tof_data_buf[2];





/* USER CODE END 0 */



/**

  * @brief  The application entry point.

  * @retval int

  */

int main(void)

{



  /* USER CODE BEGIN 1 */



  /* USER CODE END 1 */



  /* MCU Configuration--------------------------------------------------------*/



  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */

  HAL_Init();



  /* USER CODE BEGIN Init */



  /* USER CODE END Init */



  /* Configure the system clock */

  SystemClock_Config();



  /* USER CODE BEGIN SysInit */



  /* USER CODE END SysInit */



  /* Initialize all configured peripherals */

  MX_GPIO_Init();

  MX_ETH_Init();

  MX_USART3_UART_Init();

  MX_USB_OTG_FS_PCD_Init();

  MX_TIM1_Init();

  MX_TIM3_Init();

  MX_TIM4_Init();

  MX_TIM5_Init();

  MX_TIM2_Init();

  MX_I2C1_Init();

  MX_I2C2_Init();

  MX_USART2_UART_Init();

  MX_TIM9_Init();

  /* USER CODE BEGIN 2 */

  HAL_GPIO_WritePin(GPIOF, GPIO_PIN_12, GPIO_PIN_RESET);

  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15, GPIO_PIN_RESET);

  HAL_GPIO_WritePin(GPIOG, GPIO_PIN_1, GPIO_PIN_RESET);

  HAL_GPIO_WritePin(GPIOD, GPIO_PIN_4, GPIO_PIN_RESET);

  HAL_GPIO_WritePin(GPIOE, GPIO_PIN_6, GPIO_PIN_SET);



  // 모터 1

  HAL_TIM_Encoder_Start(&htim3, TIM_CHANNEL_ALL);

  HAL_TIM_Encoder_Start(&htim4, TIM_CHANNEL_ALL);

  HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_1);

  HAL_TIM_IC_Start_IT(&htim2, TIM_CHANNEL_2);

  //HAL_TIM_IC_Start_IT(&htim9, TIM_CHANNEL_1);



  Start_Rail_Motor_Timer();



  HAL_TIM_PWM_Start(&htim5, TIM_CHANNEL_1);

  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);

  HAL_TIM_PWM_Start(&htim5, TIM_CHANNEL_4);

  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);



  ROS_Comm_Init(); //usart3

  HAL_UART_Receive_IT(&huart2, &rx_data, 1);





  /* USER CODE END 2 */



  /* Infinite loop */

  /* USER CODE BEGIN WHILE */

  while (1)

  {

    /* USER CODE END WHILE */



    /* USER CODE BEGIN 3 */



    currentTime = HAL_GetTick();



    // 긴급 정지 로직

    if(emergency_stop){

        target_lin_motor = 0.0f;

        target_ang_motor = 0.0f;

        target_rail_motor = 0.0f;

        target_rpm_m1 = 0.0f;

        target_rpm_m2 = 0.0f;



        __HAL_TIM_SET_COMPARE(&htim5, TIM_CHANNEL_1, 0);

        __HAL_TIM_SET_COMPARE(&htim5, TIM_CHANNEL_4, 0);

        __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_1, 0);

        __HAL_TIM_SET_COMPARE(&htim1, TIM_CHANNEL_2, 0);



        HAL_Delay(10);

        continue;

    }





    ROS_Comm_Parse();

    Process_Auto_Rail_Control();



    // 명령 타임아웃 세이프티

    if (is_auto_rail_active == 0 &&(currentTime - lastCommandReceiveTime > 5000)) {

        target_lin_motor = 0.0f;

        target_ang_motor = 0.0f;

        target_rail_motor = 0.0f;

        target_rpm_m1 = 0.0f;

        target_rpm_m2 = 0.0f;

        target_rpm_rm1 = 0.0f;

        target_rpm_rm2 = 0.0f;

        control_m1 = 0.0f;

        control_m2 = 0.0f;

    }



    Set_Motor_Velocity(target_lin_motor, target_ang_motor);

    Set_Rail_Velocity(target_rail_motor);



    // -----------------------------------------------------------------

     // [블록 1] 메인 휠 모터 제어 및 오도메트리 연산 (100ms 주기)

    // -----------------------------------------------------------------

    static uint32_t last_test_time = 0;

    static int16_t prev_m1_cnt = 0, prev_m2_cnt = 0;

    static float integral_diff = 0.0f;



    if (HAL_GetTick() - last_test_time >= 100) {

        uint32_t now = HAL_GetTick();

        float dt = (float)(now - last_test_time) / 1000.0f;

        if (dt <= 0.0f) dt = 0.001f;



        int16_t cur_m1_cnt = (int16_t)__HAL_TIM_GET_COUNTER(&htim3);

        int16_t cur_m2_cnt = -(int16_t)__HAL_TIM_GET_COUNTER(&htim4);



        int16_t d_m1 = cur_m1_cnt - prev_m1_cnt;

        int16_t d_m2 = cur_m2_cnt - prev_m2_cnt;



        float rpm_m1 = ((float)d_m1 / 16384.0f) * (60.0f / dt);

        float rpm_m2 = ((float)d_m2 / 16384.0f) * (60.0f / dt);



        float Kp_sync = 0.8f;

        float Ki_sync = 0.05f;



        float target_diff = target_rpm_m1 - target_rpm_m2;

        float actual_diff = rpm_m1 - rpm_m2;





        float error_diff = fabs(target_diff) - fabs(actual_diff);



        integral_diff += error_diff * dt;

        if (target_rpm_m1 == 0.0f && target_rpm_m2 == 0.0f){

        	integral_diff = 0.0f;

        }



        float sync_comp = (Kp_sync * error_diff) + (Ki_sync * integral_diff);



        control_m1 = (target_rpm_m1 * 9.0f) - sync_comp;

        control_m2 = (target_rpm_m2 * 8.0f) - sync_comp;



        //DIRECTION

        if (control_m1 >= 0.0f) {

            HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14, GPIO_PIN_SET);

        } else {

            HAL_GPIO_WritePin(GPIOD, GPIO_PIN_14, GPIO_PIN_RESET);

            control_m1 = -control_m1;

        }



        if (control_m2 >= 0.0f) {

            HAL_GPIO_WritePin(GPIOG, GPIO_PIN_3, GPIO_PIN_RESET);

        } else {

            HAL_GPIO_WritePin(GPIOG, GPIO_PIN_3, GPIO_PIN_SET);

            control_m2 = -control_m2;

        }



        if (fabs(target_rpm_m1) < 0.01f && fabs(target_rpm_m2) < 0.01f) {

            control_m1 = 0.0f;

            control_m2 = 0.0f;

        }



        uint16_t pwm_m1_out = (uint16_t)(control_m1 > 1000.0f ? 1000 : control_m1);

        uint16_t pwm_m2_out = (uint16_t)(control_m2 > 1000.0f ? 1000 : control_m2);



        __HAL_TIM_SET_COMPARE(&htim5, TIM_CHANNEL_1, pwm_m1_out);

        __HAL_TIM_SET_COMPARE(&htim5, TIM_CHANNEL_4, pwm_m2_out);



        float rads_m1 = rpm_m1 * (2.0f * PI / 60.0f);

        float rads_m2 = rpm_m2 * (2.0f * PI / 60.0f);



        float ms_m1 = rads_m1 * WHEEL_RADIUS_M;

        float ms_m2 = rads_m2 * WHEEL_RADIUS_M;





        if (is_auto_rail_active == 0){



        		// 1. 엔코더 기반 이동 거리 (d_m1, d_m2를 이용)

			float delta_dist_m1 = ((float)d_m1 / 16384.0f) * (2.0f * PI * WHEEL_RADIUS_M);

			float delta_dist_m2 = ((float)d_m2 / 16384.0f) * (2.0f * PI * WHEEL_RADIUS_M);



			// 로봇 중심의 이동 거리 (선형 변위)

			float delta_dist_center = (delta_dist_m1 + delta_dist_m2) / 2.0f;



			// 2. 엔코더 기반 회전 각도 변화량 (각변위)

			// 우측 바퀴가 M1, 좌측 바퀴가 M2라고 가정했을 때의 표준 식: (우측 - 좌측) / 윤거

			float delta_theta_enc = (delta_dist_m1 - delta_dist_m2) / TRACK_WIDTH_M;



			// 3. 중간각(Mid-point) 방식을 이용한 정밀한 X, Y 좌표 누적

			float theta_mid_enc = odom_theta_enc + (delta_theta_enc * 0.5f);



			odom_x += delta_dist_center * cosf(theta_mid_enc);

			odom_y += delta_dist_center * sinf(theta_mid_enc);



			// 4. 엔코더 방향각 누적 및 정규화 (-PI ~ PI 범위 제한)

			odom_theta_enc += delta_theta_enc;



			while (odom_theta_enc > PI)  odom_theta_enc -= 2.0f * PI;

			while (odom_theta_enc < -PI) odom_theta_enc += 2.0f * PI;



			// ========================================================

			// [추가된 부분] IMU 데이터(yaw)를 이용해 odom_theta 계산

			// ========================================================

			odom_theta = yaw ;



			// IMU 각도도 동일하게 -PI ~ PI 범위로 정규화

			while (odom_theta > PI)  odom_theta -= 2.0f * PI;

			while (odom_theta < -PI) odom_theta += 2.0f * PI;



			// 두 각도의 오차 계산 (비교용)

			float theta_diff = odom_theta_enc - odom_theta;

			while (theta_diff > PI)  theta_diff -= 2.0f * PI;

			while (theta_diff < -PI) theta_diff += 2.0f * PI;



			// 5. 속도 계산 (출력용)

			float avg_lin_main = (ms_m1 + ms_m2) / 2.0f;

			float avg_ang_main = (-ms_m1 + ms_m2) / TRACK_WIDTH_M;



			// ROS_Debug_RPM(rpm_m1, rpm_m2, control_m1, control_m2, sync_comp);

			// ROS_Debug_Main(avg_lin_main, avg_ang_main, ms_m1, ms_m2, error_diff);



			// 1. 오도메트리 퍼블리시 (이미 구현된 함수)

			// ROS_Send_Odometry(odom_x, odom_y, odom_theta_enc, avg_lin_main, avg_ang_main);



			// 2. THETA 디버그용 퍼블리시

			//ROS_Debug_Theta(odom_theta_enc, odom_theta);



			// 3. WHEEL 속도 퍼블리시

			ROS_Send_Wheel(ms_m1, ms_m2);



			// 4. IMU 데이터 퍼블리시

			ROS_Send_IMU(roll, pitch, yaw);

        }



        prev_m1_cnt = cur_m1_cnt;

        prev_m2_cnt = cur_m2_cnt;

        last_test_time = now;

    }



    Update_Rail_Motor_Control();

  }







  /* USER CODE END 3 */

}



/**

  * @brief System Clock Configuration

  * @retval None

  */

void SystemClock_Config(void)

{

  RCC_OscInitTypeDef RCC_OscInitStruct = {0};

  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};



  /** Configure the main internal regulator output voltage

  */

  __HAL_RCC_PWR_CLK_ENABLE();

  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);



  /** Initializes the RCC Oscillators according to the specified parameters

  * in the RCC_OscInitTypeDef structure.

  */

  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;

  RCC_OscInitStruct.HSEState = RCC_HSE_BYPASS;

  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;

  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;

  RCC_OscInitStruct.PLL.PLLM = 4;

  RCC_OscInitStruct.PLL.PLLN = 168;

  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;

  RCC_OscInitStruct.PLL.PLLQ = 7;

  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)

  {

    Error_Handler();

  }



  /** Initializes the CPU, AHB and APB buses clocks

  */

  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK

                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;

  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;

  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;

  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;

  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;



  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)

  {

    Error_Handler();

  }

}



/**

  * @brief ETH Initialization Function

  * @param None

  * @retval None

  */

static void MX_ETH_Init(void)

{



  /* USER CODE BEGIN ETH_Init 0 */



  /* USER CODE END ETH_Init 0 */



   static uint8_t MACAddr[6];



  /* USER CODE BEGIN ETH_Init 1 */



  /* USER CODE END ETH_Init 1 */

  heth.Instance = ETH;

  MACAddr[0] = 0x00;

  MACAddr[1] = 0x80;

  MACAddr[2] = 0xE1;

  MACAddr[3] = 0x00;

  MACAddr[4] = 0x00;

  MACAddr[5] = 0x00;

  heth.Init.MACAddr = &MACAddr[0];

  heth.Init.MediaInterface = HAL_ETH_RMII_MODE;

  heth.Init.TxDesc = DMATxDscrTab;

  heth.Init.RxDesc = DMARxDscrTab;

  heth.Init.RxBuffLen = 1524;



  /* USER CODE BEGIN MACADDRESS */



  /* USER CODE END MACADDRESS */



  if (HAL_ETH_Init(&heth) != HAL_OK)

  {

    Error_Handler();

  }



  memset(&TxConfig, 0 , sizeof(ETH_TxPacketConfig));

  TxConfig.Attributes = ETH_TX_PACKETS_FEATURES_CSUM | ETH_TX_PACKETS_FEATURES_CRCPAD;

  TxConfig.ChecksumCtrl = ETH_CHECKSUM_IPHDR_PAYLOAD_INSERT_PHDR_CALC;

  TxConfig.CRCPadCtrl = ETH_CRC_PAD_INSERT;

  /* USER CODE BEGIN ETH_Init 2 */



  /* USER CODE END ETH_Init 2 */



}



/**

  * @brief I2C1 Initialization Function

  * @param None

  * @retval None

  */

static void MX_I2C1_Init(void)

{



  /* USER CODE BEGIN I2C1_Init 0 */



  /* USER CODE END I2C1_Init 0 */



  /* USER CODE BEGIN I2C1_Init 1 */



  /* USER CODE END I2C1_Init 1 */

  hi2c1.Instance = I2C1;

  hi2c1.Init.ClockSpeed = 100000;

  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;

  hi2c1.Init.OwnAddress1 = 0;

  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;

  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;

  hi2c1.Init.OwnAddress2 = 0;

  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;

  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;

  if (HAL_I2C_Init(&hi2c1) != HAL_OK)

  {

    Error_Handler();

  }



  /** Configure Analogue filter

  */

  if (HAL_I2CEx_ConfigAnalogFilter(&hi2c1, I2C_ANALOGFILTER_ENABLE) != HAL_OK)

  {

    Error_Handler();

  }



  /** Configure Digital filter

  */

  if (HAL_I2CEx_ConfigDigitalFilter(&hi2c1, 0) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN I2C1_Init 2 */



  /* USER CODE END I2C1_Init 2 */



}



/**

  * @brief I2C2 Initialization Function

  * @param None

  * @retval None

  */

static void MX_I2C2_Init(void)

{



  /* USER CODE BEGIN I2C2_Init 0 */



  /* USER CODE END I2C2_Init 0 */



  /* USER CODE BEGIN I2C2_Init 1 */



  /* USER CODE END I2C2_Init 1 */

  hi2c2.Instance = I2C2;

  hi2c2.Init.ClockSpeed = 100000;

  hi2c2.Init.DutyCycle = I2C_DUTYCYCLE_2;

  hi2c2.Init.OwnAddress1 = 0;

  hi2c2.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;

  hi2c2.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;

  hi2c2.Init.OwnAddress2 = 0;

  hi2c2.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;

  hi2c2.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;

  if (HAL_I2C_Init(&hi2c2) != HAL_OK)

  {

    Error_Handler();

  }



  /** Configure Analogue filter

  */

  if (HAL_I2CEx_ConfigAnalogFilter(&hi2c2, I2C_ANALOGFILTER_ENABLE) != HAL_OK)

  {

    Error_Handler();

  }



  /** Configure Digital filter

  */

  if (HAL_I2CEx_ConfigDigitalFilter(&hi2c2, 0) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN I2C2_Init 2 */



  /* USER CODE END I2C2_Init 2 */



}



/**

  * @brief TIM1 Initialization Function

  * @param None

  * @retval None

  */

static void MX_TIM1_Init(void)

{



  /* USER CODE BEGIN TIM1_Init 0 */



  /* USER CODE END TIM1_Init 0 */



  TIM_MasterConfigTypeDef sMasterConfig = {0};

  TIM_OC_InitTypeDef sConfigOC = {0};

  TIM_BreakDeadTimeConfigTypeDef sBreakDeadTimeConfig = {0};



  /* USER CODE BEGIN TIM1_Init 1 */



  /* USER CODE END TIM1_Init 1 */

  htim1.Instance = TIM1;

  htim1.Init.Prescaler = 1679;

  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;

  htim1.Init.Period = 999;

  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

  htim1.Init.RepetitionCounter = 0;

  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

  if (HAL_TIM_PWM_Init(&htim1) != HAL_OK)

  {

    Error_Handler();

  }

  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;

  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;

  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)

  {

    Error_Handler();

  }

  sConfigOC.OCMode = TIM_OCMODE_PWM1;

  sConfigOC.Pulse = 0;

  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;

  sConfigOC.OCNPolarity = TIM_OCNPOLARITY_HIGH;

  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;

  sConfigOC.OCIdleState = TIM_OCIDLESTATE_RESET;

  sConfigOC.OCNIdleState = TIM_OCNIDLESTATE_RESET;

  if (HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)

  {

    Error_Handler();

  }

  if (HAL_TIM_PWM_ConfigChannel(&htim1, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)

  {

    Error_Handler();

  }

  sBreakDeadTimeConfig.OffStateRunMode = TIM_OSSR_DISABLE;

  sBreakDeadTimeConfig.OffStateIDLEMode = TIM_OSSI_DISABLE;

  sBreakDeadTimeConfig.LockLevel = TIM_LOCKLEVEL_OFF;

  sBreakDeadTimeConfig.DeadTime = 0;

  sBreakDeadTimeConfig.BreakState = TIM_BREAK_DISABLE;

  sBreakDeadTimeConfig.BreakPolarity = TIM_BREAKPOLARITY_HIGH;

  sBreakDeadTimeConfig.AutomaticOutput = TIM_AUTOMATICOUTPUT_DISABLE;

  if (HAL_TIMEx_ConfigBreakDeadTime(&htim1, &sBreakDeadTimeConfig) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN TIM1_Init 2 */



  /* USER CODE END TIM1_Init 2 */

  HAL_TIM_MspPostInit(&htim1);



}



/**

  * @brief TIM2 Initialization Function

  * @param None

  * @retval None

  */

static void MX_TIM2_Init(void)

{



  /* USER CODE BEGIN TIM2_Init 0 */



  /* USER CODE END TIM2_Init 0 */



  TIM_MasterConfigTypeDef sMasterConfig = {0};

  TIM_IC_InitTypeDef sConfigIC = {0};



  /* USER CODE BEGIN TIM2_Init 1 */



  /* USER CODE END TIM2_Init 1 */

  htim2.Instance = TIM2;

  htim2.Init.Prescaler = 83;

  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;

  htim2.Init.Period = 4294967295;

  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

  if (HAL_TIM_IC_Init(&htim2) != HAL_OK)

  {

    Error_Handler();

  }

  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;

  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;

  if (HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig) != HAL_OK)

  {

    Error_Handler();

  }

  sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;

  sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;

  sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;

  sConfigIC.ICFilter = 0;

  if (HAL_TIM_IC_ConfigChannel(&htim2, &sConfigIC, TIM_CHANNEL_1) != HAL_OK)

  {

    Error_Handler();

  }

  sConfigIC.ICFilter = 15;

  if (HAL_TIM_IC_ConfigChannel(&htim2, &sConfigIC, TIM_CHANNEL_2) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN TIM2_Init 2 */



  /* USER CODE END TIM2_Init 2 */



}



/**

  * @brief TIM3 Initialization Function

  * @param None

  * @retval None

  */

static void MX_TIM3_Init(void)

{



  /* USER CODE BEGIN TIM3_Init 0 */



  /* USER CODE END TIM3_Init 0 */



  TIM_Encoder_InitTypeDef sConfig = {0};

  TIM_MasterConfigTypeDef sMasterConfig = {0};



  /* USER CODE BEGIN TIM3_Init 1 */



  /* USER CODE END TIM3_Init 1 */

  htim3.Instance = TIM3;

  htim3.Init.Prescaler = 0;

  htim3.Init.CounterMode = TIM_COUNTERMODE_UP;

  htim3.Init.Period = 65535;

  htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

  htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

  sConfig.EncoderMode = TIM_ENCODERMODE_TI12;

  sConfig.IC1Polarity = TIM_ICPOLARITY_RISING;

  sConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;

  sConfig.IC1Prescaler = TIM_ICPSC_DIV1;

  sConfig.IC1Filter = 0;

  sConfig.IC2Polarity = TIM_ICPOLARITY_RISING;

  sConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;

  sConfig.IC2Prescaler = TIM_ICPSC_DIV1;

  sConfig.IC2Filter = 0;

  if (HAL_TIM_Encoder_Init(&htim3, &sConfig) != HAL_OK)

  {

    Error_Handler();

  }

  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;

  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;

  if (HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN TIM3_Init 2 */



  /* USER CODE END TIM3_Init 2 */



}



/**

  * @brief TIM4 Initialization Function

  * @param None

  * @retval None

  */

static void MX_TIM4_Init(void)

{



  /* USER CODE BEGIN TIM4_Init 0 */



  /* USER CODE END TIM4_Init 0 */



  TIM_Encoder_InitTypeDef sConfig = {0};

  TIM_MasterConfigTypeDef sMasterConfig = {0};



  /* USER CODE BEGIN TIM4_Init 1 */



  /* USER CODE END TIM4_Init 1 */

  htim4.Instance = TIM4;

  htim4.Init.Prescaler = 0;

  htim4.Init.CounterMode = TIM_COUNTERMODE_UP;

  htim4.Init.Period = 65535;

  htim4.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

  htim4.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

  sConfig.EncoderMode = TIM_ENCODERMODE_TI12;

  sConfig.IC1Polarity = TIM_ICPOLARITY_RISING;

  sConfig.IC1Selection = TIM_ICSELECTION_DIRECTTI;

  sConfig.IC1Prescaler = TIM_ICPSC_DIV1;

  sConfig.IC1Filter = 0;

  sConfig.IC2Polarity = TIM_ICPOLARITY_RISING;

  sConfig.IC2Selection = TIM_ICSELECTION_DIRECTTI;

  sConfig.IC2Prescaler = TIM_ICPSC_DIV1;

  sConfig.IC2Filter = 0;

  if (HAL_TIM_Encoder_Init(&htim4, &sConfig) != HAL_OK)

  {

    Error_Handler();

  }

  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;

  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;

  if (HAL_TIMEx_MasterConfigSynchronization(&htim4, &sMasterConfig) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN TIM4_Init 2 */



  /* USER CODE END TIM4_Init 2 */



}



/**

  * @brief TIM5 Initialization Function

  * @param None

  * @retval None

  */

static void MX_TIM5_Init(void)

{



  /* USER CODE BEGIN TIM5_Init 0 */



  /* USER CODE END TIM5_Init 0 */



  TIM_MasterConfigTypeDef sMasterConfig = {0};

  TIM_OC_InitTypeDef sConfigOC = {0};



  /* USER CODE BEGIN TIM5_Init 1 */



  /* USER CODE END TIM5_Init 1 */

  htim5.Instance = TIM5;

  htim5.Init.Prescaler = 3;

  htim5.Init.CounterMode = TIM_COUNTERMODE_UP;

  htim5.Init.Period = 999;

  htim5.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

  htim5.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

  if (HAL_TIM_PWM_Init(&htim5) != HAL_OK)

  {

    Error_Handler();

  }

  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;

  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;

  if (HAL_TIMEx_MasterConfigSynchronization(&htim5, &sMasterConfig) != HAL_OK)

  {

    Error_Handler();

  }

  sConfigOC.OCMode = TIM_OCMODE_PWM1;

  sConfigOC.Pulse = 0;

  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;

  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;

  if (HAL_TIM_PWM_ConfigChannel(&htim5, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)

  {

    Error_Handler();

  }

  if (HAL_TIM_PWM_ConfigChannel(&htim5, &sConfigOC, TIM_CHANNEL_4) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN TIM5_Init 2 */



  /* USER CODE END TIM5_Init 2 */

  HAL_TIM_MspPostInit(&htim5);



}



/**

  * @brief TIM9 Initialization Function

  * @param None

  * @retval None

  */

static void MX_TIM9_Init(void)

{



  /* USER CODE BEGIN TIM9_Init 0 */



  /* USER CODE END TIM9_Init 0 */



  TIM_IC_InitTypeDef sConfigIC = {0};



  /* USER CODE BEGIN TIM9_Init 1 */



  /* USER CODE END TIM9_Init 1 */

  htim9.Instance = TIM9;

  htim9.Init.Prescaler = 167;

  htim9.Init.CounterMode = TIM_COUNTERMODE_UP;

  htim9.Init.Period = 65535;

  htim9.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

  htim9.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;

  if (HAL_TIM_IC_Init(&htim9) != HAL_OK)

  {

    Error_Handler();

  }

  sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_RISING;

  sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;

  sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;

  sConfigIC.ICFilter = 0;

  if (HAL_TIM_IC_ConfigChannel(&htim9, &sConfigIC, TIM_CHANNEL_1) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN TIM9_Init 2 */



  /* USER CODE END TIM9_Init 2 */



}



/**

  * @brief USART2 Initialization Function

  * @param None

  * @retval None

  */

static void MX_USART2_UART_Init(void)

{



  /* USER CODE BEGIN USART2_Init 0 */



  /* USER CODE END USART2_Init 0 */



  /* USER CODE BEGIN USART2_Init 1 */



  /* USER CODE END USART2_Init 1 */

  huart2.Instance = USART2;

  huart2.Init.BaudRate = 115200;

  huart2.Init.WordLength = UART_WORDLENGTH_8B;

  huart2.Init.StopBits = UART_STOPBITS_1;

  huart2.Init.Parity = UART_PARITY_NONE;

  huart2.Init.Mode = UART_MODE_TX_RX;

  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;

  huart2.Init.OverSampling = UART_OVERSAMPLING_16;

  if (HAL_UART_Init(&huart2) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN USART2_Init 2 */



  /* USER CODE END USART2_Init 2 */



}



/**

  * @brief USART3 Initialization Function

  * @param None

  * @retval None

  */

static void MX_USART3_UART_Init(void)

{



  /* USER CODE BEGIN USART3_Init 0 */



  /* USER CODE END USART3_Init 0 */



  /* USER CODE BEGIN USART3_Init 1 */



  /* USER CODE END USART3_Init 1 */

  huart3.Instance = USART3;

  huart3.Init.BaudRate = 230400;

  huart3.Init.WordLength = UART_WORDLENGTH_8B;

  huart3.Init.StopBits = UART_STOPBITS_1;

  huart3.Init.Parity = UART_PARITY_NONE;

  huart3.Init.Mode = UART_MODE_TX_RX;

  huart3.Init.HwFlowCtl = UART_HWCONTROL_NONE;

  huart3.Init.OverSampling = UART_OVERSAMPLING_16;

  if (HAL_UART_Init(&huart3) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN USART3_Init 2 */



  /* USER CODE END USART3_Init 2 */



}



/**

  * @brief USB_OTG_FS Initialization Function

  * @param None

  * @retval None

  */

static void MX_USB_OTG_FS_PCD_Init(void)

{



  /* USER CODE BEGIN USB_OTG_FS_Init 0 */



  /* USER CODE END USB_OTG_FS_Init 0 */



  /* USER CODE BEGIN USB_OTG_FS_Init 1 */



  /* USER CODE END USB_OTG_FS_Init 1 */

  hpcd_USB_OTG_FS.Instance = USB_OTG_FS;

  hpcd_USB_OTG_FS.Init.dev_endpoints = 4;

  hpcd_USB_OTG_FS.Init.speed = PCD_SPEED_FULL;

  hpcd_USB_OTG_FS.Init.dma_enable = DISABLE;

  hpcd_USB_OTG_FS.Init.phy_itface = PCD_PHY_EMBEDDED;

  hpcd_USB_OTG_FS.Init.Sof_enable = ENABLE;

  hpcd_USB_OTG_FS.Init.low_power_enable = DISABLE;

  hpcd_USB_OTG_FS.Init.lpm_enable = DISABLE;

  hpcd_USB_OTG_FS.Init.vbus_sensing_enable = ENABLE;

  hpcd_USB_OTG_FS.Init.use_dedicated_ep1 = DISABLE;

  if (HAL_PCD_Init(&hpcd_USB_OTG_FS) != HAL_OK)

  {

    Error_Handler();

  }

  /* USER CODE BEGIN USB_OTG_FS_Init 2 */



  /* USER CODE END USB_OTG_FS_Init 2 */



}



/**

  * @brief GPIO Initialization Function

  * @param None

  * @retval None

  */

static void MX_GPIO_Init(void)

{

  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* USER CODE BEGIN MX_GPIO_Init_1 */



  /* USER CODE END MX_GPIO_Init_1 */



  /* GPIO Ports Clock Enable */

  __HAL_RCC_GPIOE_CLK_ENABLE();

  __HAL_RCC_GPIOC_CLK_ENABLE();

  __HAL_RCC_GPIOF_CLK_ENABLE();

  __HAL_RCC_GPIOH_CLK_ENABLE();

  __HAL_RCC_GPIOA_CLK_ENABLE();

  __HAL_RCC_GPIOB_CLK_ENABLE();

  __HAL_RCC_GPIOG_CLK_ENABLE();

  __HAL_RCC_GPIOD_CLK_ENABLE();



  /*Configure GPIO pin Output Level */

  HAL_GPIO_WritePin(GPIOE, RELAY_PC_Pin|RELAY_Pin, GPIO_PIN_SET);



  /*Configure GPIO pin Output Level */

  HAL_GPIO_WritePin(GPIOB, LD1_Pin|LD3_Pin|LD2_Pin, GPIO_PIN_RESET);



  /*Configure GPIO pin Output Level */

  HAL_GPIO_WritePin(GPIOF, START_Pin|RAIL2_FR_Pin, GPIO_PIN_RESET);



  /*Configure GPIO pin Output Level */

  HAL_GPIO_WritePin(GPIOG, M2_BRAKE_Pin|M2_CW_Pin, GPIO_PIN_RESET);



  /*Configure GPIO pin Output Level */

  HAL_GPIO_WritePin(TRIG_GPIO_Port, TRIG_Pin, GPIO_PIN_RESET);



  /*Configure GPIO pin Output Level */

  HAL_GPIO_WritePin(GPIOD, M1_CW_Pin|BRAKE_Pin|STARTD4_Pin, GPIO_PIN_RESET);



  /*Configure GPIO pin Output Level */

  HAL_GPIO_WritePin(GPIOC, RAIL1_FR_Pin|GPIO_PIN_9, GPIO_PIN_RESET);



  /*Configure GPIO pins : RELAY_PC_Pin RELAY_Pin TRIG_Pin */

  GPIO_InitStruct.Pin = RELAY_PC_Pin|RELAY_Pin|TRIG_Pin;

  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;

  GPIO_InitStruct.Pull = GPIO_NOPULL;

  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

  HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);



  /*Configure GPIO pin : USER_Btn_Pin */

  GPIO_InitStruct.Pin = USER_Btn_Pin;

  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;

  GPIO_InitStruct.Pull = GPIO_NOPULL;

  HAL_GPIO_Init(USER_Btn_GPIO_Port, &GPIO_InitStruct);



  /*Configure GPIO pin : RAIL2_SPD_Pin */

  GPIO_InitStruct.Pin = RAIL2_SPD_Pin;

  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;

  GPIO_InitStruct.Pull = GPIO_PULLUP;

  HAL_GPIO_Init(RAIL2_SPD_GPIO_Port, &GPIO_InitStruct);



  /*Configure GPIO pins : LD1_Pin LD3_Pin LD2_Pin */

  GPIO_InitStruct.Pin = LD1_Pin|LD3_Pin|LD2_Pin;

  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;

  GPIO_InitStruct.Pull = GPIO_NOPULL;

  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);



  /*Configure GPIO pins : START_Pin RAIL2_FR_Pin */

  GPIO_InitStruct.Pin = START_Pin|RAIL2_FR_Pin;

  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;

  GPIO_InitStruct.Pull = GPIO_NOPULL;

  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

  HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);



  /*Configure GPIO pins : M2_BRAKE_Pin M2_CW_Pin */

  GPIO_InitStruct.Pin = M2_BRAKE_Pin|M2_CW_Pin;

  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;

  GPIO_InitStruct.Pull = GPIO_NOPULL;

  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

  HAL_GPIO_Init(GPIOG, &GPIO_InitStruct);



  /*Configure GPIO pin : RAIL1_SPD_Pin */

  GPIO_InitStruct.Pin = RAIL1_SPD_Pin;

  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;

  GPIO_InitStruct.Pull = GPIO_PULLUP;

  HAL_GPIO_Init(RAIL1_SPD_GPIO_Port, &GPIO_InitStruct);



  /*Configure GPIO pins : M1_CW_Pin BRAKE_Pin STARTD4_Pin */

  GPIO_InitStruct.Pin = M1_CW_Pin|BRAKE_Pin|STARTD4_Pin;

  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;

  GPIO_InitStruct.Pull = GPIO_NOPULL;

  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

  HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);



  /*Configure GPIO pin : USB_OverCurrent_Pin */

  GPIO_InitStruct.Pin = USB_OverCurrent_Pin;

  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;

  GPIO_InitStruct.Pull = GPIO_NOPULL;

  HAL_GPIO_Init(USB_OverCurrent_GPIO_Port, &GPIO_InitStruct);



  /*Configure GPIO pins : RAIL1_FR_Pin PC9 */

  GPIO_InitStruct.Pin = RAIL1_FR_Pin|GPIO_PIN_9;

  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;

  GPIO_InitStruct.Pull = GPIO_NOPULL;

  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);



  /* EXTI interrupt init*/

  HAL_NVIC_SetPriority(EXTI9_5_IRQn, 0, 0);

  HAL_NVIC_EnableIRQ(EXTI9_5_IRQn);



  HAL_NVIC_SetPriority(EXTI15_10_IRQn, 0, 0);

  HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);



  /* USER CODE BEGIN MX_GPIO_Init_2 */



  /* USER CODE END MX_GPIO_Init_2 */

}



/* USER CODE BEGIN 4 */

void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart)

{

    // IMU 센서(USART2)에서 오버런 에러 등이 발생했을 때 수신 인터럽트 재활성화

    if (huart->Instance == USART2)

    {

        HAL_UART_Receive_IT(&huart2, &rx_data, 1);

    }



}





void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)

{

    if (huart->Instance == USART3)

    {

        if (received_byte != '\r' && received_byte != '\n')

        {

            if (rx_count < ROS_CMD_BUFFER_SIZE - 1)

            {

                ros_rx_buffer[rx_count++] = received_byte;

            }

        }

        else // Enter(\r 또는 \n)가 입력된 경우

        {



            if (rx_count > 0)

            {

                ros_rx_buffer[rx_count] = '\0';

                cmd_received = 1; // 여기서 플래그가 켜집니다!

            }

        }

        // 다음 1바이트 수신 대기 (필수)

        HAL_UART_Receive_IT(&huart3, &received_byte, 1);

    }



    if (huart->Instance == USART2)

	{

		// 1. 헤더(0x55) 동기화 대기

		if (rx_index == 0)

		{

			if (rx_data == 0x55)

			{

				rx_buffer[rx_index++] = rx_data;

			}

		}

		// 2. 헤더가 맞으면 나머지 10바이트 수신

		else

		{

			rx_buffer[rx_index++] = rx_data;



			// 11바이트가 모두 모였을 때

			if (rx_index >= 11)

			{

				rx_index = 0; // 다음 패킷 수신을 위해 인덱스 초기화



				// 데이터 파싱 (0x53은 각도 데이터 패킷을 의미함)

				if (rx_buffer[1] == 0x53)

				{

					// Checksum 검증 (선택사항이지만 데이터 신뢰성을 위해 권장)

					uint8_t sum = 0;

					for (int i = 0; i < 10; i++) sum += rx_buffer[i];



					if (sum == rx_buffer[10])

					{

						// Roll, Pitch, Yaw 계산 (라디안 단위로 바로 변환)

						// PI 매크로가 정의되어 있지 않다면 3.14159265f 를 직접 적어주셔도 됩니다.

						roll  = ((short)(rx_buffer[3] << 8 | rx_buffer[2])) / 32768.0f * PI;

						pitch = ((short)(rx_buffer[5] << 8 | rx_buffer[4])) / 32768.0f * PI;

						yaw   = ((short)(rx_buffer[7] << 8 | rx_buffer[6])) / 32768.0f * PI;

					}

				}

			}

		}



		// 다음 1바이트 수신을 위해 인터럽트 재활성화 (필수)

		HAL_UART_Receive_IT(&huart2, &rx_data, 1);

	}

}





void HAL_GPIO_EXTI_Callback(uint16_t GPIO_PIN){



    if (GPIO_PIN == USER_Btn_Pin){

        // 비상정지 상태 토글 (0 -> 1 -> 0)

        emergency_stop = !emergency_stop;



        if(emergency_stop){



            sprintf(uart_buf, "\r\n[!] EMERGENCY STOP [!]\r\n");

        } else {

            // 재가동 시 초기 상태 설정 및 타이머 초기화

            sprintf(uart_buf, "\r\n[>] SYSTEM RESUME [>]\r\n");

        }

        HAL_UART_Transmit(&huart3, (uint8_t*)uart_buf, strlen(uart_buf), 10);

    }



    /*if (GPIO_PIN == RAIL1_SPD_Pin || GPIO_PIN == RAIL2_SPD_Pin) {

		Rail_Motor_EXTI_Handler(GPIO_PIN);

	}*/

}

/* USER CODE END 4 */



/**

  * @brief  This function is executed in case of error occurrence.

  * @retval None

  */

void Error_Handler(void)

{

  /* USER CODE BEGIN Error_Handler_Debug */

  /* User can add his own implementation to report the HAL error return state */

  __disable_irq();

  while (1)

  {

  }

  /* USER CODE END Error_Handler_Debug */

}

#ifdef USE_FULL_ASSERT

/**

  * @brief  Reports the name of the source file and the source line number

  *         where the assert_param error has occurred.

  * @param  file: pointer to the source file name

  * @param  line: assert_param error line source number

  * @retval None

  */

void assert_failed(uint8_t *file, uint32_t line)

{

  /* USER CODE BEGIN 6 */

  /* User can add his own implementation to report the file name and line number,

     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */

  /* USER CODE END 6 */

}

#endif /* USE_FULL_ASSERT */