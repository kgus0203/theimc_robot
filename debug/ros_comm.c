/*

 * ros_comm.c

 *

 *  Created on: Jun 29, 2026

 *      Author: jeff

 */



#include "ros_comm.h"

#include <string.h>

#include <stdio.h>

#include <stdlib.h>



uint32_t last_toggle_time = 0;

extern uint8_t is_auto_rail_active;



void Set_Main_Brake(GPIO_PinState state) {

    HAL_GPIO_WritePin(GPIOD, GPIO_PIN_15, state);

    HAL_GPIO_WritePin(GPIOG, GPIO_PIN_1, state);

}



void ROS_Comm_Init(void){

	HAL_UART_Receive_IT(&huart3, &received_byte, 1);

}



void ROS_Comm_Parse(void){



    // ROS 통신 파싱 명령

    if (cmd_received)

    {

        cmd_received = 0;

        char parsing_buffer[ROS_CMD_BUFFER_SIZE] = {0};

        strncpy(parsing_buffer, (char*)ros_rx_buffer, ROS_CMD_BUFFER_SIZE - 1);

        char *token;

        char cmd_type[10] = "";





        token = strtok(parsing_buffer, ",");

        if (token != NULL) {

            strncpy(cmd_type, token, sizeof(cmd_type) - 1);



            if (strcmp(cmd_type, "CMD") == 0) {

                token = strtok(NULL, ",");

                if (token != NULL) {

                	float temp_lin = atof(token);

                    token = strtok(NULL, ",");

                    if (token != NULL) {

                    	float temp_ang = atof(token);

                    	if (is_auto_rail_active == 0){

                    		target_lin_motor = temp_lin;

							target_ang_motor = temp_ang;

							lastCommandReceiveTime = currentTime;

							Set_Main_Brake(GPIO_PIN_RESET);

                    	}

                    }

                }

            }

            else if (strcmp(cmd_type, "RAIL") == 0) {

                token = strtok(NULL, ",");

                if (token != NULL) {

                    target_rail_motor = atof(token);

                    lastCommandReceiveTime = currentTime;

                }

            }

            else if (strcmp(cmd_type, "DETECTED") == 0) {

            	ROS_Send_State("OUT_RAIL");

            	is_auto_rail_active = 1;



            	Set_Main_Brake(GPIO_PIN_RESET);

                rail_motor_state = 0;

                target_rail_motor = 0.0f;

                target_lin_motor = 0.15f;

                last_toggle_time = currentTime;

                lastCommandReceiveTime = currentTime;

            }

            else if (strcmp(cmd_type, "OUT") == 0) {

				// 1. ROS 상태 전송

				ROS_Send_State("OUT_RAIL");



				Set_Main_Brake(GPIO_PIN_RESET);

				target_rail_motor = 0.0f;

				target_lin_motor = 0.0f;

				target_ang_motor = 0.0f;

				is_auto_rail_active = 0;



				last_toggle_time = currentTime;

				lastCommandReceiveTime = currentTime;

			}

            else if (strcmp(cmd_type, "ON") == 0) {

				// 1. ROS 상태 전송

				ROS_Send_State("ON_RAIL");

				target_rail_motor = 0.0f;

				target_lin_motor = 0.0f;

				target_ang_motor = 0.0f;

				Set_Main_Brake(GPIO_PIN_SET);

				is_auto_rail_active = 1;

				rail_motor_state = 3;



				last_toggle_time = currentTime;

				lastCommandReceiveTime = currentTime;

			}

            else if (strcmp(cmd_type, "FORWARD") == 0) {

            	Set_Main_Brake(GPIO_PIN_SET);

                target_rail_motor = 0.2f;

                lastCommandReceiveTime = currentTime;

            }

            else if (strcmp(cmd_type, "BACK") == 0) {

            	Set_Main_Brake(GPIO_PIN_SET);

                target_rail_motor = -0.3f;

                lastCommandReceiveTime = currentTime;

            }

            else if (strcmp(cmd_type, "STOP") == 0) {

            	Set_Main_Brake(GPIO_PIN_SET);

                target_rail_motor = 0.0f;

                lastCommandReceiveTime = currentTime;

            }



        }

        memset(ros_rx_buffer, 0, ROS_CMD_BUFFER_SIZE);

        rx_count = 0;

    }



}



void ROS_Send_State(const char* state){

	sprintf(uart_buf, "STATE,%s\r\n", state);

	HAL_UART_Transmit(&huart3, (uint8_t*)uart_buf, strlen(uart_buf), 10);

}



void ROS_Send_Odometry(float odom_x, float odom_y, float odom_theta, float linear_vel, float angular_vel) {

    sprintf(uart_buf, "ODOM,%.3f,%.3f,%.3f,%.3f,%.3f\r\n",

            odom_x, odom_y, odom_theta, linear_vel, angular_vel);

    HAL_UART_Transmit(&huart3, (uint8_t*)uart_buf, strlen(uart_buf), 100);

}



void ROS_Send_Wheel(float ms_m1, float ms_m2) {

    sprintf(uart_buf, "WHEEL,%.3f,%.3f\r\n", ms_m1, ms_m2);

    HAL_UART_Transmit(&huart3, (uint8_t*)uart_buf, strlen(uart_buf), 10);

}



// IMU 데이터 퍼블리시

void ROS_Send_IMU(float roll, float pitch, float yaw) {

    sprintf(uart_buf, "IMU,%.2f,%.2f,%.2f\r\n", roll, pitch, yaw);

    HAL_UART_Transmit(&huart3, (uint8_t*)uart_buf, strlen(uart_buf), 10);

}



// [디버그] THETA 각도 비교 출력

void ROS_Debug_Theta(float odom_theta_enc, float odom_theta) {

    sprintf(uart_buf, "[THETA] ENC: %.3f rad (%.1f deg) | IMU: %.3f rad (%.1f deg) | Diff: %.3f\r\n",

            odom_theta_enc, odom_theta_enc * (180.0f / PI),

            odom_theta, odom_theta * (180.0f / PI),

            odom_theta_enc - odom_theta);

    HAL_UART_Transmit(&huart3, (uint8_t*)uart_buf, strlen(uart_buf), 100);

}



// [디버그] RPM 및 제어량 출력

void ROS_Debug_RPM(float rpm_m1, float rpm_m2, float control_m1, float control_m2, float sync_comp) {

    sprintf(uart_buf, "RPM (M1:%.2f, M2:%.2f)| control_m1: %.2f  | control_m2: %.2f | ERROR: %.2f\r\n",

            rpm_m1, rpm_m2, control_m1, control_m2, sync_comp);

    HAL_UART_Transmit(&huart3, (uint8_t*)uart_buf, strlen(uart_buf), 100);

}



// [디버그] MAIN 선속도/각속도 출력

void ROS_Debug_Main(float avg_lin, float avg_ang, float ms_m1, float ms_m2, float error_diff) {

    sprintf(uart_buf, "[MAIN] Lin: %.2f m/s | Ang: %.2f rad/s (M1:%.2f, M2:%.2f) | ERROR: %.2f\r\n",

            avg_lin, avg_ang, ms_m1, ms_m2, error_diff);

    HAL_UART_Transmit(&huart3, (uint8_t*)uart_buf, strlen(uart_buf), 100);

}



void TOF_dist(float distance_mm){

	sprintf(uart_buf, "TOF: %.2f mm\r\n", distance_mm);

	HAL_UART_Transmit(&huart3, (uint8_t*)uart_buf, strlen(uart_buf), 10);

}

