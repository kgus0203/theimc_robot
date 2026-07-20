/*

 * sensor_process.c

 *

 *  Created on: Jun 29, 2026

 *      Author: jeff

 */





#include "sensor_process.h"

#include "motor_control.h"

extern void ROS_Send_State(char *state);

extern void TOF_dist(float distance_mm);



extern uint32_t last_toggle_time;

extern I2C_HandleTypeDef hi2c1;

extern uint32_t lastCommandReceiveTime;



float roll = 0.0f;

float pitch = 0.0f;

float yaw = 0.0f;

float odom_theta = 0.0f;

uint8_t is_imu_initialized = 0;

float imu_yaw_offset = 0.0f;



uint16_t tof_distance_mm = 0;

float current_tof_distance = 800.0f;



float Read_TOF_Distance(I2C_HandleTypeDef *hi2c){

	uint8_t tof_data_buf[2] = {0,};
	float distance_mm = 800.0f;

	// I2C로 ToF 센서 데이터 읽기
	HAL_StatusTypeDef status = HAL_I2C_Mem_Read(hi2c, TOF10120_ADDR, TOF10120_DIST_REG, I2C_MEMADD_SIZE_8BIT, tof_data_buf, 2, 5);

	// 읽기 성공 여부에 따라 거리 계산

	if (status == HAL_OK) {

		// High Byte와 Low Byte를 합쳐 16비트 거리 값(mm)으로 계산

		tof_distance_mm = (tof_data_buf[0] << 8) | tof_data_buf[1];

		distance_mm = (float)tof_distance_mm;

	}



	return distance_mm;





}



void Process_Auto_Rail_Control(void){
	if(is_auto_rail_active == 0) return;
	uint32_t currentTime = HAL_GetTick();
	static uint32_t last_adc_time = 0;
	static int current_publish_state = 0; //0:OUT_RAIL 1:ON_RAILTOF_dist

	if (currentTime - last_adc_time >= 100){
		float distance_mm = Read_TOF_Distance(&hi2c1);
		TOF_dist(distance_mm);
		int target_publish_state = current_publish_state;
		if(rail_motor_state == 0 || rail_motor_state ==5 ){
			ROS_Send_State("OUT_RAIL");
		}

		else if (rail_motor_state == 2 || rail_motor_state ==3 ){
			ROS_Send_State("ON_RAIL");
		}

		else if (rail_motor_state == 1){
			ROS_Send_State("ENTERING");
		}

		else if (rail_motor_state == 4){
			ROS_Send_State("EXITING");
		}





		// state machine

		// 0: 레일 진입 감지

		if (rail_motor_state == 0 && distance_mm <= 130.0f) {

			target_lin_motor = 0.0f;

			rail_motor_state = 1;

			last_toggle_time = currentTime;

		}

		// 1: 레일 위로 안착 대기

		else if (rail_motor_state == 1) {

			if (currentTime - last_toggle_time >= 2000) {
				// 일정시간이 지나면 그냥 안착했다 생각하고 레일바퀴를 돌림


				//HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15, GPIO_PIN_SET); // BRAKE

				//HAL_GPIO_WritePin(GPIOG, GPIO_PIN_1, GPIO_PIN_SET);  // BRAKE

				target_rail_motor = 0.2f;

				rail_motor_state = 2;

				last_toggle_time = currentTime;

			}

		}

		// 2: 레일 주행 (2초 후 속도 0)

		else if (rail_motor_state == 2) {

			if (currentTime - last_toggle_time >= 2000) {
				//2초 주행이 끝나면 속도를 0으로 하고 브레이크를 걸어 레일 위에서 정지
				HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15, GPIO_PIN_SET); // BRAKE

				HAL_GPIO_WritePin(GPIOG, GPIO_PIN_1, GPIO_PIN_SET);  // BRAKE

				target_rail_motor = 0.0f;

				rail_motor_state = 3;

			}

		}

		// 3: 레일 이탈 감지 대기

		else if (rail_motor_state == 3) {

			if (distance_mm <= 130.0f) {

				rail_motor_state = 4;

				target_lin_motor = 0.0f;

				target_ang_motor = 0.0f;

				target_rail_motor = 0.0f;

				lastCommandReceiveTime = currentTime; // 타임아웃 방지

			}

		}

		// 4: 마무리 및 후진

		else if (rail_motor_state == 4) {

			lastCommandReceiveTime = currentTime;

			HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15, GPIO_PIN_RESET);

			HAL_GPIO_WritePin(GPIOG, GPIO_PIN_1, GPIO_PIN_RESET);

			target_lin_motor = -0.15f;

			target_rail_motor = 0.0f;

			rail_motor_state = 5;



		}

		else if (rail_motor_state == 5 && distance_mm >= 140.0f) {



			is_auto_rail_active = 0; // 모드 종료

			rail_motor_state = 0;



		}





		last_adc_time = currentTime;

	}



}

